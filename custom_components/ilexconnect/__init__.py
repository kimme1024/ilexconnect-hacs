import logging
import async_timeout
from datetime import timedelta

from homeassistant import config_entries, core
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

API_URL = "https://i-lexconnect.com/api/devices/{device_id}/live"
AUTH_URL = "https://i-lexconnect.com/login"

class IlexConnectApiClient:
    """API client for I-LexConnect."""

    def __init__(self, hass: core.HomeAssistant, username: str, password: str, device_id: str):
        self._session = aiohttp_client.async_get_clientsession(hass)
        self.username = username
        self.password = password
        self.device_id = device_id
        self.token = None

    async def authenticate(self):
        """Authenticate with the I-LexConnect server."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.post(
                    AUTH_URL,
                    json={"username": self.username, "password": self.password},
                )
                data = await response.json()
                if response.status == 200:
                    self.token = data.get("token")
                    _LOGGER.info("Authenticated with I-LexConnect API")
                else:
                    raise UpdateFailed(f"Authentication failed: {response.status}")
        except Exception as e:
            _LOGGER.error("Authentication error: %s", e)
            raise UpdateFailed(f"Authentication error: {e}")

    async def get_device_data(self):
        """Fetch live data from the water softener."""
        if not self.token:
            await self.authenticate()

        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        url = API_URL.format(device_id=self.device_id)

        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(url, headers=headers)
                if response.status == 401:  # Token expired
                    await self.authenticate()
                    headers = {"Authorization": f"Bearer {self.token}"}
                    response = await self._session.get(url, headers=headers)
                
                if response.status != 200:
                    raise UpdateFailed(f"Failed to retrieve device data: {response.status}")
                return await response.json()
        except Exception as e:
            _LOGGER.error("Error fetching device data: %s", e)
            raise UpdateFailed(f"Error fetching device data: {e}")

async def async_setup_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    """Set up I-LexConnect from a config entry."""
    # Haal polling interval op (altijd omzetten naar int voor de zekerheid)
    interval_seconds = int(entry.options.get("update_interval", DEFAULT_UPDATE_INTERVAL.total_seconds()))
    
    api_client = IlexConnectApiClient(
        hass, entry.data["username"], entry.data["password"], entry.data["device_id"]
    )

    async def async_update_data():
        return await api_client.get_device_data()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=interval_seconds),
    )

    await coordinator.async_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    
    # Registreer de listener voor wijzigingen in opties
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True

async def async_unload_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok

async def update_listener(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)