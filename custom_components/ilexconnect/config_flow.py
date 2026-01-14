import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("device_id"): str,
})

OPTIONS_SCHEMA = vol.Schema({
    vol.Optional("update_interval", default=DEFAULT_UPDATE_INTERVAL.total_seconds()): int
})

class IlexConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="I-LexConnect", data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

    @callback
    def async_get_options_flow(self, config_entry):
        return IlexConnectOptionsFlowHandler(config_entry)

class IlexConnectOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        options = {"update_interval": self.config_entry.options.get("update_interval", DEFAULT_UPDATE_INTERVAL.total_seconds())}
        return self.async_show_form(step_id="init", data_schema=vol.Schema({
            vol.Optional("update_interval", default=options["update_interval"]): int
        }))