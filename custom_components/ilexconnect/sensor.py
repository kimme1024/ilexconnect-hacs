from datetime import datetime
import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, SENSOR_KEYS

_LOGGER = logging.getLogger(__name__)

# Metadata labels voor de systeemsensoren
META_KEYS_LABELS = {
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

    # Sla de array-velden over (ruwe data)
    skip_keys = ["getTCG", "getYCG", "getMCG", "getRCG", "getSCG", "getWCG", "getLCG"]
    
    for key, (label, unit) in SENSOR_KEYS.items():
        if key in skip_keys:
            continue
        entities.append(IlexSensor(coordinator, key, label, unit))

    # Voeg de meta-data sensoren toe
    for key, label in META_KEYS_LABELS.items():
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
        # Terug naar het originele ID formaat voor een schone installatie
        return f"ilexconnect_{self._key}"

    @property
    def native_unit_of_measurement(self):
        # Forceer de correcte eenheid voor het Energy Dashboard
        if self._key == "getRCG_total":
            return "m³"
        return self._unit

    @property
    def native_value(self):
        data = self.coordinator.data
        if not data:
            return None
            
        value = data.get(self._key)
        if value is None:
            return None

        # Verwerking van tijdstempel sensoren
        if self._key in ["getDAT", "date"]:
            try:
                return datetime.utcfromtimestamp(int(value))
            except (ValueError, TypeError):
                return value

        # Zorg dat alle numerieke waarden als float worden doorgegeven
        try:
            return float(value)
        except (ValueError, TypeError):
            return value

    @property
    def suggested_display_precision(self):
        # Toon 3 decimalen voor de watermeter (liternauwkeurigheid)
        if self._key == "getRCG_total":
            return 3
        return None

    @property
    def device_class(self):
        # De 'water' klasse is essentieel voor herkenning in het Energy Dashboard
        if self._key == "getRCG_total":
            return SensorDeviceClass.WATER
        return None

    @property
    def state_class(self):
        # 'total_increasing' geeft aan dat dit een cumulatieve teller is
        if self._key == "getRCG_total":
            return SensorStateClass.TOTAL_INCREASING
        return None

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