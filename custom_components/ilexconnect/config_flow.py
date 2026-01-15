import logging
import voluptuous as vol
from datetime import timedelta

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class IlexConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for I-LexConnect."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="I-LexConnect", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                    vol.Required("device_id"): str,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Return the options flow handler."""
        # We geven GEEN config_entry mee aan de constructor
        return IlexConnectOptionsFlowHandler()


class IlexConnectOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle the options flow."""

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # De config_entry is binnen een OptionsFlow ALTIJD beschikbaar via self._config_entry
        # Dit is de standaard methode binnen Home Assistant
        options = self.config_entry.options
        
        current_val = options.get(
            "update_interval", int(DEFAULT_UPDATE_INTERVAL.total_seconds())
        )
        
        # Veiligheid voor het geval er nog een timedelta object rondslingert
        if isinstance(current_val, timedelta):
            current_val = int(current_val.total_seconds())

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional("update_interval", default=int(current_val)): int,
                }
            ),
        )