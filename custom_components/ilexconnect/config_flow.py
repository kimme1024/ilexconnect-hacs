import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Schema voor de gebruiker
DATA_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("device_id"): str,
})

class IlexConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for I-LexConnect."""

    VERSION = 1
    # Settings-icoon verbergen
    _hassio = False
    _async_available = True

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Maak direct een entry aan
            return self.async_create_entry(title="I-LexConnect", data=user_input)

        # Toon het formulier aan de gebruiker
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)