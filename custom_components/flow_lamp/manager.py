"""Per-lamp cycle manager: warm-up, maintain, taper, runtime limit, cooldown."""
from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Callable, Iterable, Mapping
from datetime import datetime, timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import CALLBACK_TYPE, Event, EventStateChangedData, HomeAssistant, callback
from homeassistant.helpers.event import (
    async_call_later,
    async_track_state_change_event,
    async_track_time_interval,
)
from homeassistant.helpers.start import async_at_started
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .const import (
    BRIGHTNESS_TOLERANCE_PCT,
    COLOR_KEYS,
    CONF_DIMMING,
    CONF_LIGHT,
    CONF_LIQUID_CLEAR,
    CONF_LIQUID_COLOR,
    CONF_WAX_COLOR,
    DEFAULTS,
    DIMMING_AUTO,
    DIMMING_NO,
    DIMMING_YES,
    DOMAIN,
    OFF_DEBOUNCE_SECONDS,
    STAGE_COOLDOWN,
    STAGE_IDLE,
    STAGE_RUNNING,
    STORAGE_VERSION,
    TICK_SECONDS,
)
from .logic import Profile, display_state, target_pct

_LOGGER = logging.getLogger(__name__)


class FlowLampManager:
    """Owns the cycle state for one lamp."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self.light: str = entry.data[CONF_LIGHT]
        self.domain: str = self.light.split(".")[0]
        self.profile = Profile.from_mapping(entry.options)
        self._timing_sig = self.options_signature(entry.options)
        self._store: Store = Store(hass, STORAGE_VERSION, f"{DOMAIN}.{entry.entry_id}")

        self.enabled = True
        self.stage = STAGE_IDLE
        self.cycle_start: datetime | None = None
        self.cooldown_until: datetime | None = None

        self._lock = asyncio.Lock()
        self._listeners: list[CALLBACK_TYPE] = []
        self._unsubs: list[CALLBACK_TYPE] = []
        self._debounce: CALLBACK_TYPE | None = None

    # ---- options -----------------------------------------------------
    @staticmethod
    def options_signature(options: Mapping[str, Any]) -> str:
        """Everything except cosmetic colours; a change here needs a reload."""
        return json.dumps({k: v for k, v in options.items() if k not in COLOR_KEYS}, sort_keys=True, default=str)

    def options_are_cosmetic(self) -> bool:
        return self.options_signature(self.entry.options) == self._timing_sig

    @property
    def dimmable(self) -> bool:
        """Can the lamp's output be dimmed (and so tapered)?"""
        mode = self.entry.options.get(CONF_DIMMING, DIMMING_AUTO)
        if self.domain != "light" or mode == DIMMING_NO:
            return False
        if mode == DIMMING_YES:
            return True
        state = self.hass.states.get(self.light)
        modes = state.attributes.get("supported_color_modes") if state else None
        if not modes:
            return True  # unknown (e.g. not loaded yet): assume it can dim
        return any(str(m) != "onoff" for m in modes)

    @property
    def wax_color(self) -> list[int]:
        return [int(v) for v in self.entry.options.get(CONF_WAX_COLOR, DEFAULTS[CONF_WAX_COLOR])]

    @property
    def liquid_color(self) -> list[int]:
        return [int(v) for v in self.entry.options.get(CONF_LIQUID_COLOR, DEFAULTS[CONF_LIQUID_COLOR])]

    @property
    def liquid_clear(self) -> bool:
        return bool(self.entry.options.get(CONF_LIQUID_CLEAR, False))

    @callback
    def async_set_colors(
        self,
        *,
        wax: Iterable[int] | None = None,
        liquid: Iterable[int] | None = None,
        clear: bool | None = None,
    ) -> None:
        options = dict(self.entry.options)
        if wax is not None:
            options[CONF_WAX_COLOR] = [int(v) for v in wax]
        if liquid is not None:
            options[CONF_LIQUID_COLOR] = [int(v) for v in liquid]
        if clear is not None:
            options[CONF_LIQUID_CLEAR] = bool(clear)
        self.hass.config_entries.async_update_entry(self.entry, options=options)

    @callback
    def async_refresh(self) -> None:
        """Push a cosmetic change (colours) to the entities without a reload."""
        self._notify()

    # ---- persistence -------------------------------------------------
    async def async_load(self) -> None:
        data = await self._store.async_load() or {}
        self.enabled = data.get("enabled", True)
        self.stage = data.get("stage", STAGE_IDLE)
        self.cycle_start = dt_util.parse_datetime(data["cycle_start"]) if data.get("cycle_start") else None
        self.cooldown_until = dt_util.parse_datetime(data["cooldown_until"]) if data.get("cooldown_until") else None

    def _as_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "stage": self.stage,
            "cycle_start": self.cycle_start.isoformat() if self.cycle_start else None,
            "cooldown_until": self.cooldown_until.isoformat() if self.cooldown_until else None,
        }

    def _save(self) -> None:
        self._store.async_delay_save(self._as_dict, 5)

    # ---- lifecycle ---------------------------------------------------
    async def async_start(self) -> None:
        self._unsubs.append(
            async_track_state_change_event(self.hass, [self.light], self._handle_light_event)
        )
        self._unsubs.append(
            async_track_time_interval(self.hass, self.async_evaluate, timedelta(seconds=TICK_SECONDS))
        )
        # Runs immediately if HA is already up, otherwise once startup completes.
        self._unsubs.append(async_at_started(self.hass, self.async_evaluate))

    async def async_stop(self) -> None:
        for unsub in self._unsubs:
            unsub()
        self._unsubs.clear()
        if self._debounce:
            self._debounce()
            self._debounce = None
        await self._store.async_save(self._as_dict())

    # ---- listeners for entities -------------------------------------
    @callback
    def async_add_listener(self, cb: Callable[[], None]) -> CALLBACK_TYPE:
        self._listeners.append(cb)

        @callback
        def _remove() -> None:
            if cb in self._listeners:
                self._listeners.remove(cb)

        return _remove

    @callback
    def _notify(self) -> None:
        for cb in list(self._listeners):
            cb()

    # ---- derived values ---------------------------------------------
    @property
    def lamp_on(self) -> bool | None:
        state = self.hass.states.get(self.light)
        if state is None or state.state not in (STATE_ON, STATE_OFF):
            return None
        return state.state == STATE_ON

    @property
    def elapsed_min(self) -> float | None:
        if self.stage != STAGE_RUNNING or self.cycle_start is None:
            return None
        return (dt_util.utcnow() - self.cycle_start).total_seconds() / 60

    @property
    def target_brightness_pct(self) -> int | None:
        elapsed = self.elapsed_min
        return None if elapsed is None or not self.dimmable else target_pct(self.profile, elapsed)

    @property
    def display_state(self) -> str:
        return display_state(self.stage, self.elapsed_min, self.profile.warmup_min)

    @property
    def dimming_level(self) -> int | None:
        """Actual dimmer output in %, read from the light (0 when off)."""
        state = self.hass.states.get(self.light)
        if state is None or state.state not in (STATE_ON, STATE_OFF):
            return None
        if state.state == STATE_OFF:
            return 0
        brightness = state.attributes.get("brightness")
        return 100 if brightness is None else round(brightness / 255 * 100)

    @property
    def minutes_remaining(self) -> int:
        """Runtime left while running, cooldown left while cooling down, else 0."""
        if self.stage == STAGE_RUNNING and self.elapsed_min is not None:
            return max(0, round(self.profile.max_run_min - self.elapsed_min))
        if self.stage == STAGE_COOLDOWN and self.cooldown_until:
            return max(0, round((self.cooldown_until - dt_util.utcnow()).total_seconds() / 60))
        return 0

    # ---- controls ----------------------------------------------------
    async def async_set_enabled(self, enabled: bool) -> None:
        async with self._lock:
            self.enabled = enabled
            if not enabled:
                # Disabling drops any cycle so a stale clock can't misfire later.
                self.stage = STAGE_IDLE
                self.cycle_start = None
                self.cooldown_until = None
            self._save()
            self._notify()
        if enabled:
            await self.async_evaluate()

    async def async_power(self, on: bool) -> None:
        """Turn the lamp on/off (errors propagate to the caller)."""
        await self._call_light("turn_on" if on else "turn_off", blocking=True)

    # ---- event handling ----------------------------------------------
    @callback
    def _handle_light_event(self, event: Event[EventStateChangedData]) -> None:
        old, new = event.data["old_state"], event.data["new_state"]
        if new is None:
            return
        if old is not None and old.state == new.state:
            self._notify()  # attribute-only change (brightness): refresh sensors, no cycle logic
            return
        if new.state == STATE_OFF and self.stage == STAGE_RUNNING:
            # Debounce so a brief off blip doesn't trigger a full cooldown.
            if self._debounce:
                self._debounce()
            self._debounce = async_call_later(self.hass, OFF_DEBOUNCE_SECONDS, self._debounced)
        else:
            self.hass.async_create_task(self.async_evaluate())

    async def _debounced(self, _now: datetime) -> None:
        self._debounce = None
        await self.async_evaluate()

    async def async_evaluate(self, *_: Any) -> None:
        async with self._lock:
            await self._evaluate()
            self._notify()

    async def _call_light(self, service: str, *, blocking: bool = False, **data: Any) -> None:
        if not self.dimmable:
            data.pop("brightness_pct", None)
            data.pop("transition", None)
        await self.hass.services.async_call(
            self.domain, service, {"entity_id": self.light, **data}, blocking=blocking
        )

    def _begin_cooldown(self, now: datetime) -> None:
        self.stage = STAGE_COOLDOWN
        self.cooldown_until = now + timedelta(minutes=self.profile.cooldown_min)
        self.cycle_start = None
        self._save()

    def _reset(self) -> None:
        self.stage = STAGE_IDLE
        self.cycle_start = None
        self.cooldown_until = None
        self._save()

    async def _evaluate(self) -> None:
        if not self.enabled:
            return
        state = self.hass.states.get(self.light)
        if state is None or state.state not in (STATE_ON, STATE_OFF):
            return  # unavailable/unknown: keep the clock running, act when it's back
        on = state.state == STATE_ON
        now = dt_util.utcnow()
        p = self.profile

        # Cooldown expired -> idle
        if self.stage == STAGE_COOLDOWN and (self.cooldown_until is None or now >= self.cooldown_until):
            self.stage = STAGE_IDLE
            self.cooldown_until = None
            self._save()

        if self.stage == STAGE_IDLE:
            if on:
                self.stage = STAGE_RUNNING
                self.cycle_start = now
                self._save()
                if self.dimmable:
                    await self._call_light("turn_on", brightness_pct=p.warm_pct, transition=2)

        elif self.stage == STAGE_COOLDOWN:
            if on:
                _LOGGER.debug("%s turned on during cooldown, switching off", self.light)
                await self._call_light("turn_off")

        elif self.stage == STAGE_RUNNING:
            if self.cycle_start is None:
                self.cycle_start = now
                self._save()
            elapsed = (now - self.cycle_start).total_seconds() / 60
            if not on:
                if elapsed < p.warmup_min:
                    self._reset()  # turned off before warm-up finished: no cooldown
                else:
                    self._begin_cooldown(now)  # turned off mid-cycle
            elif elapsed >= p.max_run_min:
                self._begin_cooldown(now)  # set stage first so the off event is a no-op
                await self._call_light("turn_off")
            elif self.dimmable:
                target = target_pct(p, elapsed)
                brightness = state.attributes.get("brightness")
                current = None if brightness is None else round(brightness / 255 * 100)
                if current is None or abs(current - target) > BRIGHTNESS_TOLERANCE_PCT:
                    await self._call_light("turn_on", brightness_pct=target, transition=30)


type FlowLampConfigEntry = ConfigEntry[FlowLampManager]
