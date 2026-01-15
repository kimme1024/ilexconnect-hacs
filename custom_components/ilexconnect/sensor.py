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
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = f"{DOMAIN}_{key}"

    @property
    def native_value(self):
        data = self.coordinator.data
        if not data or self._key not in data:
            return None
            
        value = data.get(self._key)

        # 1. Tijdstempel verwerking
        if self._key in ["getDAT", "date"]:
            try:
                return datetime.utcfromtimestamp(int(value))
            except (ValueError, TypeError):
                return value

        # 2. Numerieke verwerking & Conversie van m3 naar Liter
        try:
            float_value = float(value)
            
            # De SYR API levert deze keys in m3, we rekenen ze hier om naar L
            if self._key in ["getRCG_total", "getMCG_total", "getMCG", "getRCG"]:
                return round(float_value * 1000, 1)
                
            return float_value
        except (ValueError, TypeError):
            return value

    @property
    def device_class(self):
        if self._key in ["getRCG_total", "getMCG_total", "getTCG_total", "getWCG_total"]:
            return SensorDeviceClass.WATER
        return None

    @property
    def state_class(self):
        if self._key in ["getRCG_total", "getMCG_total", "getTCG_total", "getWCG_total"]:
            return SensorStateClass.TOTAL_INCREASING
        return None

    @property
    def suggested_display_precision(self):
        if self.native_unit_of_measurement == "L":
            return 1
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