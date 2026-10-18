"""Constants for Flow Lamp."""
from __future__ import annotations

from typing import Any

DOMAIN = "flow_lamp"

CONF_LIGHT = "light"
CONF_WARM_PCT = "warm_pct"
CONF_MAINTAIN_PCT = "maintain_pct"
CONF_FLOOR_PCT = "floor_pct"
CONF_WARMUP_MIN = "warmup_min"
CONF_HOLD_MIN = "hold_min"
CONF_MAX_RUN_MIN = "max_run_min"
CONF_COOLDOWN_MIN = "cooldown_min"
CONF_WAX_COLOR = "wax_color"
CONF_LIQUID_COLOR = "liquid_color"
CONF_LIQUID_CLEAR = "liquid_clear"
CONF_DIMMING = "dimming"

# Placeholders: set these from the lamp manual / by watching the lamp.
DEFAULTS: dict[str, Any] = {
    CONF_WARM_PCT: 100,
    CONF_MAINTAIN_PCT: 70,
    CONF_FLOOR_PCT: 45,
    CONF_WARMUP_MIN: 90,
    CONF_HOLD_MIN: 60,
    CONF_MAX_RUN_MIN: 480,
    CONF_COOLDOWN_MIN: 240,
    CONF_WAX_COLOR: [255, 214, 51],  # yellow wax (looks red once backlit)
    CONF_LIQUID_COLOR: [122, 43, 191],  # purple liquid
    CONF_LIQUID_CLEAR: False,
    CONF_DIMMING: "auto",
}

# Option changes in this group never need the entry to be reloaded.
COLOR_KEYS = ("wax_color", "liquid_color", "liquid_clear")

DIMMING_AUTO = "auto"
DIMMING_YES = "yes"
DIMMING_NO = "no"

# Presets offered by the Wax color / Liquid color select entities.
# Exact values can still be set from Configure ("Custom" is shown for those).
COLOR_PRESETS: dict[str, list[int]] = {
    "yellow": [255, 214, 51],
    "orange": [255, 140, 26],
    "red": [225, 40, 45],
    "pink": [245, 95, 165],
    "purple": [122, 43, 191],
    "blue": [60, 110, 255],
    "teal": [25, 185, 185],
    "green": [60, 195, 90],
    "white": [250, 248, 240],
}
WAX_OPTIONS = [*COLOR_PRESETS, "custom"]
LIQUID_OPTIONS = ["clear", *[c for c in COLOR_PRESETS if c != "white"], "custom"]

STAGE_IDLE = "idle"
STAGE_RUNNING = "running"
STAGE_COOLDOWN = "cooldown"

# What the State sensor shows (warm-up and the maintain/taper phases are all "flowing")
DISPLAY_OFF = "off"
DISPLAY_WARM_UP = "warm_up"
DISPLAY_FLOWING = "flowing"
DISPLAY_COOL_DOWN = "cool_down"
DISPLAY_STATES = [DISPLAY_OFF, DISPLAY_WARM_UP, DISPLAY_FLOWING, DISPLAY_COOL_DOWN]

TICK_SECONDS = 60
OFF_DEBOUNCE_SECONDS = 3
BRIGHTNESS_TOLERANCE_PCT = 2
STORAGE_VERSION = 1
