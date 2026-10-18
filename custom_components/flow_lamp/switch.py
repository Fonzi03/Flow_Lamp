"""Switches: lamp power and cycle management on/off."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON, STATE_UNAVAILABLE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, STAGE_COOLDOWN
from .entity import FlowLampEntity
from .logic import format_remaining
from .manager import FlowLampConfigEntry, FlowLampManager


async def async_setup_entry(
    hass: HomeAssistant, entry: FlowLampConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    manager = entry.runtime_data
    async_add_entities([FlowLampPowerSwitch(manager), FlowLampEnabledSwitch(manager)])


class FlowLampPowerSwitch(FlowLampEntity, SwitchEntity):
    """Turns the lamp itself on/off (what tapping the card does)."""

    def __init__(self, manager: FlowLampManager) -> None:
        super().__init__(manager, "power")

    @property
    def available(self) -> bool:
        state = self.hass.states.get(self.manager.light)
        return state is not None and state.state != STATE_UNAVAILABLE

    @property
    def is_on(self) -> bool:
        state = self.hass.states.get(self.manager.light)
        return state is not None and state.state == STATE_ON

    async def async_turn_on(self, **kwargs: Any) -> None:
        m = self.manager
        if m.enabled and m.stage == STAGE_COOLDOWN and m.minutes_remaining > 0:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="cooldown_active",
                translation_placeholders={"remaining": format_remaining(m.minutes_remaining)},
            )
        await m.async_power(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.manager.async_power(False)


class FlowLampEnabledSwitch(FlowLampEntity, SwitchEntity):
    """Enable/disable Flow Lamp's management of this lamp."""

    def __init__(self, manager: FlowLampManager) -> None:
        super().__init__(manager, "enabled")

    @property
    def is_on(self) -> bool:
        return self.manager.enabled

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.manager.async_set_enabled(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.manager.async_set_enabled(False)
