"""Wax / liquid colour selectors (presets). Exact colours: Configure on the entry."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import COLOR_PRESETS, LIQUID_OPTIONS, WAX_OPTIONS
from .entity import FlowLampEntity
from .manager import FlowLampConfigEntry, FlowLampManager


async def async_setup_entry(
    hass: HomeAssistant, entry: FlowLampConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    manager = entry.runtime_data
    async_add_entities([FlowLampWaxColorSelect(manager), FlowLampLiquidColorSelect(manager)])


def _preset_for(rgb: list[int]) -> str:
    for name, value in COLOR_PRESETS.items():
        if list(value) == list(rgb):
            return name
    return "custom"


class FlowLampWaxColorSelect(FlowLampEntity, SelectEntity):
    _attr_options = WAX_OPTIONS

    def __init__(self, manager: FlowLampManager) -> None:
        super().__init__(manager, "wax_color")

    @property
    def current_option(self) -> str:
        return _preset_for(self.manager.wax_color)

    async def async_select_option(self, option: str) -> None:
        if option in COLOR_PRESETS:
            self.manager.async_set_colors(wax=COLOR_PRESETS[option])


class FlowLampLiquidColorSelect(FlowLampEntity, SelectEntity):
    _attr_options = LIQUID_OPTIONS

    def __init__(self, manager: FlowLampManager) -> None:
        super().__init__(manager, "liquid_color")

    @property
    def current_option(self) -> str:
        if self.manager.liquid_clear:
            return "clear"
        return _preset_for(self.manager.liquid_color)

    async def async_select_option(self, option: str) -> None:
        if option == "clear":
            self.manager.async_set_colors(clear=True)
        elif option in COLOR_PRESETS:
            self.manager.async_set_colors(liquid=COLOR_PRESETS[option], clear=False)
