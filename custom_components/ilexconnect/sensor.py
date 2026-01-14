from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, SENSOR_KEYS

# Nieuwe meta keys met Engelse labels
META_KEYS = {
    "dtype": "Device Type",
    "firmware": "Firmware",
    "getDAT": "System Date/Time",
    "getMAC": "Mac Address",
    "getSRN": "Serial Number",
    "status": "Status",
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    # Enkelvoudige sensors (numeric / string)
    for key, (label, unit) in SENSOR_KEYS.items():
        # Skip keys that are lists
        if key in ["getTCG", "getYCG", "getMCG", "getRCG", "getSCG", "getWCG", "getLCG"]:
            continue
        entities.append(IlexSensor(coordinator, key, label, unit))

    # Meta data sensors - onderaan
    for key, label in META_KEYS.items():
        entities.append(IlexSensor(coordinator, key, label, None))

    async_add_entities(entities)

class IlexSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, name, unit):
        super().__init__(coordinator)
        self._key = key
        self._name = name
        self._unit = unit

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f"ilexconnect_{self._key}"

    @property
    def native_unit_of_measurement(self):
        return self._unit

    @property
    def native_value(self):
        data = self.coordinator.data
        value = data.get(self._key)
        if value is None:
            return None

        # Convert timestamp fields to datetime
        if self._key in ["getDAT", "date", "getDATasTimestamp"]:
            try:
                return datetime.utcfromtimestamp(int(value))
            except:
                return value

        # Convert numeric fields
        try:
            return float(value)
        except:
            return value

    @property
    def device_info(self):
        data = self.coordinator.data
        return DeviceInfo(
            identifiers={(DOMAIN, data.get("getSRN"))},
            name="I-LexConnect Water Softener",
            manufacturer="SYR",
            model=data.get("dtype"),
            sw_version=data.get("firmware"),
        )