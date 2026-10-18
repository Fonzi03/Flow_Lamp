"""Pure cycle math (no Home Assistant imports, so it is easy to test)."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .const import (
    DISPLAY_COOL_DOWN,
    DISPLAY_FLOWING,
    DISPLAY_OFF,
    DISPLAY_WARM_UP,
    STAGE_COOLDOWN,
    STAGE_RUNNING,
    CONF_COOLDOWN_MIN,
    CONF_FLOOR_PCT,
    CONF_HOLD_MIN,
    CONF_MAINTAIN_PCT,
    CONF_MAX_RUN_MIN,
    CONF_WARM_PCT,
    CONF_WARMUP_MIN,
    DEFAULTS,
)


@dataclass(frozen=True)
class Profile:
    warm_pct: int
    maintain_pct: int
    floor_pct: int
    warmup_min: int
    hold_min: int
    max_run_min: int
    cooldown_min: int

    @classmethod
    def from_mapping(cls, data: Mapping) -> "Profile":
        d = {**DEFAULTS, **data}
        return cls(
            warm_pct=int(d[CONF_WARM_PCT]),
            maintain_pct=int(d[CONF_MAINTAIN_PCT]),
            floor_pct=int(d[CONF_FLOOR_PCT]),
            warmup_min=int(d[CONF_WARMUP_MIN]),
            hold_min=int(d[CONF_HOLD_MIN]),
            max_run_min=int(d[CONF_MAX_RUN_MIN]),
            cooldown_min=int(d[CONF_COOLDOWN_MIN]),
        )


def target_pct(p: Profile, elapsed_min: float) -> int:
    """Brightness target: warm-up, hold, then linear taper to the floor."""
    if elapsed_min < p.warmup_min:
        return p.warm_pct
    taper_start = p.warmup_min + p.hold_min
    if elapsed_min < taper_start:
        return p.maintain_pct
    span = p.max_run_min - taper_start
    if span <= 0:
        return p.floor_pct
    f = min(max((elapsed_min - taper_start) / span, 0.0), 1.0)
    return round(p.maintain_pct - (p.maintain_pct - p.floor_pct) * f)


def display_state(stage: str, elapsed_min: float | None, warmup_min: int) -> str:
    """Map internal stage to the user-facing state (maintain + taper = flowing)."""
    if stage == STAGE_COOLDOWN:
        return DISPLAY_COOL_DOWN
    if stage == STAGE_RUNNING:
        if elapsed_min is not None and elapsed_min < warmup_min:
            return DISPLAY_WARM_UP
        return DISPLAY_FLOWING
    return DISPLAY_OFF


def format_remaining(minutes: int) -> str:
    """'45 min' up to 59 minutes, then '1 h 30 min' / '2 h'."""
    minutes = max(0, int(minutes))
    if minutes < 60:
        return f"{minutes} min"
    hours, mins = divmod(minutes, 60)
    return f"{hours} h" if mins == 0 else f"{hours} h {mins} min"
