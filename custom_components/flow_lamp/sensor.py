"""Dimming level, state and time-remaining sensors."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DISPLAY_STATES, DOMAIN
from .entity import FlowLampEntity
from .logic import format_remaining
from .manager import FlowLampConfigEntry


async def async_setup_entry(
    hass: HomeAssistant, entry: FlowLampConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    manager = entry.runtime_data
    entities: list[SensorEntity] = [FlowLampStateSensor(manager), FlowLampRemainingSensor(manager)]
    if manager.dimmable:
        entities.insert(0, FlowLampDimmingLevelSensor(manager))
    else:
        # A lamp without dimming has no dimming level: drop a leftover entity if there is one.
        registry = er.async_get(hass)
        stale = registry.async_get_entity_id("sensor", DOMAIN, f"{entry.entry_id}_dimming_level")
        if stale:
            registry.async_remove(stale)
    async_add_entities(entities)


class FlowLampDimmingLevelSensor(FlowLampEntity, SensorEntity):
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, manager) -> None:
        super().__init__(manager, "dimming_level")

    @property
    def native_value(self) -> int | None:
        return self.manager.dimming_level

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"target_pct": self.manager.target_brightness_pct}


class FlowLampStateSensor(FlowLampEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = DISPLAY_STATES

    def __init__(self, manager) -> None:
        super().__init__(manager, "state")

    @property
    def native_value(self) -> str:
        return self.manager.display_state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        m = self.manager
        return {
            "cycle_start": m.cycle_start.isoformat() if m.cycle_start else None,
            "cooldown_until": m.cooldown_until.isoformat() if m.cooldown_until else None,
            "light": m.light,
            "dimmable": m.dimmable,
            # Read by the Flow Lamp dashboard card
            "wax_color": m.wax_color,
            "liquid_color": None if m.liquid_clear else m.liquid_color,
            "liquid_clear": m.liquid_clear,
        }


class FlowLampRemainingSensor(FlowLampEntity, SensorEntity):
    def __init__(self, manager) -> None:
        super().__init__(manager, "time_remaining")

    @property
    def native_value(self) -> str:
        return format_remaining(self.manager.minutes_remaining)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"minutes": self.manager.minutes_remaining}
