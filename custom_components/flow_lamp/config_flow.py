"""Config and options flow."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    BooleanSelector,
    ColorRGBSelector,
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_COOLDOWN_MIN,
    CONF_DIMMING,
    CONF_FLOOR_PCT,
    CONF_HOLD_MIN,
    CONF_LIGHT,
    CONF_LIQUID_CLEAR,
    CONF_LIQUID_COLOR,
    CONF_MAINTAIN_PCT,
    CONF_MAX_RUN_MIN,
    CONF_WARM_PCT,
    CONF_WARMUP_MIN,
    CONF_WAX_COLOR,
    DEFAULTS,
    DIMMING_AUTO,
    DIMMING_NO,
    DIMMING_YES,
    DOMAIN,
)

_NUMERIC = [
    CONF_WARM_PCT,
    CONF_MAINTAIN_PCT,
    CONF_FLOOR_PCT,
    CONF_WARMUP_MIN,
    CONF_HOLD_MIN,
    CONF_MAX_RUN_MIN,
    CONF_COOLDOWN_MIN,
]


def _num(lo: int, hi: int, unit: str) -> NumberSelector:
    return NumberSelector(
        NumberSelectorConfig(min=lo, max=hi, step=1, mode=NumberSelectorMode.BOX, unit_of_measurement=unit)
    )


def _option_fields() -> dict:
    return {
        vol.Required(CONF_WARM_PCT): _num(1, 100, "%"),
        vol.Required(CONF_MAINTAIN_PCT): _num(1, 100, "%"),
        vol.Required(CONF_FLOOR_PCT): _num(1, 100, "%"),
        vol.Required(CONF_WARMUP_MIN): _num(1, 720, "min"),
        vol.Required(CONF_HOLD_MIN): _num(0, 720, "min"),
        vol.Required(CONF_MAX_RUN_MIN): _num(10, 1440, "min"),
        vol.Required(CONF_COOLDOWN_MIN): _num(1, 1440, "min"),
        vol.Required(CONF_WAX_COLOR): ColorRGBSelector(),
        vol.Required(CONF_LIQUID_COLOR): ColorRGBSelector(),
        vol.Required(CONF_LIQUID_CLEAR): BooleanSelector(),
        vol.Required(CONF_DIMMING): SelectSelector(
            SelectSelectorConfig(
                options=[
                    {"value": DIMMING_AUTO, "label": "Detect automatically"},
                    {"value": DIMMING_YES, "label": "Dimmable"},
                    {"value": DIMMING_NO, "label": "On/off only"},
                ],
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
    }


def _clean(data: dict[str, Any]) -> dict[str, Any]:
    out = dict(data)
    for key in _NUMERIC:
        out[key] = int(out[key])
    for key in (CONF_WAX_COLOR, CONF_LIQUID_COLOR):
        out[key] = [max(0, min(255, int(v))) for v in out[key]]
    out[CONF_LIQUID_CLEAR] = bool(out[CONF_LIQUID_CLEAR])
    return out


def _validate(d: dict[str, Any]) -> dict[str, str]:
    if d[CONF_FLOOR_PCT] > d[CONF_MAINTAIN_PCT]:
        return {"base": "floor_above_maintain"}
    if d[CONF_WARMUP_MIN] + d[CONF_HOLD_MIN] > d[CONF_MAX_RUN_MIN]:
        return {"base": "runtime_too_short"}
    return {}


class FlowLampConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            cleaned = _clean(user_input)
            errors = _validate(cleaned)
            if not errors:
                light = cleaned.pop(CONF_LIGHT)
                await self.async_set_unique_id(light)
                self._abort_if_unique_id_configured()
                state = self.hass.states.get(light)
                name = state.name if state else light
                return self.async_create_entry(
                    title=f"{name} Flow Lamp", data={CONF_LIGHT: light}, options=cleaned
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_LIGHT): EntitySelector(EntitySelectorConfig(domain=["light", "switch"])),
                **_option_fields(),
            }
        )
        suggested = {**DEFAULTS, **(user_input or {})}
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(schema, suggested),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry) -> "FlowLampOptionsFlow":
        return FlowLampOptionsFlow()


class FlowLampOptionsFlow(OptionsFlow):
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            cleaned = _clean(user_input)
            errors = _validate(cleaned)
            if not errors:
                return self.async_create_entry(data=cleaned)

        suggested = user_input or {**DEFAULTS, **self.config_entry.options}
        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(vol.Schema(_option_fields()), suggested),
            errors=errors,
        )
