"""Flow Lamp: wax-safe runtime management for lava lamps."""
from __future__ import annotations

import logging
from pathlib import Path

import voluptuous as vol
from aiohttp import web
from homeassistant.components import websocket_api
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import HomeAssistantView
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.start import async_at_started
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util

from .manager import FlowLampConfigEntry, FlowLampManager

PLATFORMS = [Platform.SELECT, Platform.SENSOR, Platform.SWITCH]
CARD_URL = "/flow_lamp_static/flow-lamp-card.js"  # no query string: a "?v=" on the resource broke the card picker
_LOGGER = logging.getLogger(__name__)


class FlowLampCardView(HomeAssistantView):
    """Serve the card so browsers always check for a newer version.

    Without a Cache-Control header a browser may keep using an old copy of the card for days after an
    update (and the mobile app for longer). `no-cache` makes it revalidate on every load; an unchanged
    file costs only a tiny 304 reply.
    """

    url = CARD_URL
    name = "flow_lamp:card"
    requires_auth = False

    def __init__(self, path: Path) -> None:
        self._path = path

    async def get(self, request: web.Request) -> web.StreamResponse:
        return web.FileResponse(self._path, headers={"Cache-Control": "no-cache"})


@websocket_api.websocket_command({vol.Required("type"): "flow_lamp/now"})
@callback
def _ws_now(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Home Assistant's own clock, so the card's countdown never depends on the browser's time."""
    connection.send_result(msg["id"], {"now": dt_util.utcnow().isoformat()})


async def _async_ensure_card_resource(hass: HomeAssistant) -> bool:
    """Make sure the card is a Lovelace resource (storage mode only). Idempotent."""
    data = hass.data.get("lovelace")
    if data is None:
        return False
    resources = data.get("resources") if isinstance(data, dict) else getattr(data, "resources", None)
    if resources is None or not hasattr(resources, "async_create_item"):
        return False  # YAML-mode resources can't be edited
    try:
        if not getattr(resources, "loaded", True):
            await resources.async_load()
            resources.loaded = True
        for item in resources.async_items():
            if item.get("url", "").split("?")[0] == CARD_URL:
                if item["url"] != CARD_URL:  # strip any query string left by an older version
                    await resources.async_update_item(item["id"], {"res_type": "module", "url": CARD_URL})
                return True
        await resources.async_create_item({"res_type": "module", "url": CARD_URL})
        return True
    except Exception:  # noqa: BLE001 - never block setup over a dashboard nicety
        _LOGGER.warning("Could not register the Flow Lamp card as a dashboard resource", exc_info=True)
        return False


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Serve the Flow Lamp dashboard card and make sure dashboards load it."""
    websocket_api.async_register_command(hass, _ws_now)
    card = Path(__file__).parent / "www" / "flow-lamp-card.js"
    if not card.is_file():
        return True
    hass.http.register_view(FlowLampCardView(card))
    if await _async_ensure_card_resource(hass):
        return True

    async def _later(_hass: HomeAssistant) -> None:
        # Lovelace may not have been ready yet. If resources can't be edited
        # (YAML mode), fall back to loading the card as an extra frontend module.
        if not await _async_ensure_card_resource(hass):
            add_extra_js_url(hass, CARD_URL)

    async_at_started(hass, _later)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: FlowLampConfigEntry) -> bool:
    manager = FlowLampManager(hass, entry)
    await manager.async_load()
    entry.runtime_data = manager

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(manager.async_stop)
    entry.async_on_unload(entry.add_update_listener(_options_updated))

    await manager.async_start()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: FlowLampConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _options_updated(hass: HomeAssistant, entry: FlowLampConfigEntry) -> None:
    manager = entry.runtime_data
    if manager.options_are_cosmetic():
        manager.async_refresh()  # colour change only: no reload needed
    else:
        await hass.config_entries.async_reload(entry.entry_id)
