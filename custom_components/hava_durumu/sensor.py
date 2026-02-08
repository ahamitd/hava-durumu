"""Sensor platform for Hava Durumu."""
from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfLength,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, CONDITION_DESCRIPTIONS, DOMAIN
from .coordinator import HavaDurumuDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class HavaDurumuSensorEntityDescription(SensorEntityDescription):
    """Describes Hava Durumu sensor entity."""

    value_fn: Callable[[dict[str, Any]], Any] | None = None


SENSOR_DESCRIPTIONS: tuple[HavaDurumuSensorEntityDescription, ...] = (
    HavaDurumuSensorEntityDescription(
        key="temperature",
        translation_key="temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("sicaklik"),
    ),
    HavaDurumuSensorEntityDescription(
        key="humidity",
        translation_key="humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("nem"),
    ),
    HavaDurumuSensorEntityDescription(
        key="wind_speed",
        translation_key="wind_speed",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("ruzgarHiz"),
    ),
    HavaDurumuSensorEntityDescription(
        key="wind_bearing",
        translation_key="wind_bearing",
        native_unit_of_measurement="°",
        icon="mdi:compass",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("ruzgarYon"),
    ),
    HavaDurumuSensorEntityDescription(
        key="pressure",
        translation_key="pressure",
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("denizeIndirgenmisBasinc"),
    ),
    HavaDurumuSensorEntityDescription(
        key="visibility",
        translation_key="visibility",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("gorus") if data.get("gorus") and data.get("gorus") != -9999 else None,
    ),
    HavaDurumuSensorEntityDescription(
        key="precipitation_1h",
        translation_key="precipitation_1h",
        native_unit_of_measurement="mm",
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:weather-rainy",
        value_fn=lambda data: data.get("yagis1Saat") if data.get("yagis1Saat") and data.get("yagis1Saat") != -9999 else None,
    ),
    HavaDurumuSensorEntityDescription(
        key="precipitation_24h",
        translation_key="precipitation_24h",
        native_unit_of_measurement="mm",
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:weather-rainy",
        value_fn=lambda data: data.get("yagis24Saat") if data.get("yagis24Saat") and data.get("yagis24Saat") != -9999 else None,
    ),
    HavaDurumuSensorEntityDescription(
        key="cloud_coverage",
        translation_key="cloud_coverage",
        native_unit_of_measurement="okta",
        icon="mdi:cloud",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("kapalilik") if data.get("kapalilik") and data.get("kapalilik") != -9999 else None,
    ),
    HavaDurumuSensorEntityDescription(
        key="apparent_temperature",
        translation_key="apparent_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("hissedilenSicaklik"),
    ),
    HavaDurumuSensorEntityDescription(
        key="condition_text",
        translation_key="condition_text",
        icon="mdi:weather-partly-cloudy",
        value_fn=lambda data: CONDITION_DESCRIPTIONS.get(
            data.get("hadiseKodu", ""), data.get("hadiseKodu", "")
        ),
    ),
    HavaDurumuSensorEntityDescription(
        key="alert_count",
        translation_key="alert_count",
        icon="mdi:alert",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=None,  # Will be handled separately
    ),
    HavaDurumuSensorEntityDescription(
        key="alert_details",
        translation_key="alert_details",
        icon="mdi:alert-circle",
        value_fn=None,  # Will be handled separately
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hava Durumu sensor entities from a config entry."""
    coordinator: HavaDurumuDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        HavaDurumuSensor(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
    ]
    
    async_add_entities(entities)


class HavaDurumuSensor(CoordinatorEntity[HavaDurumuDataUpdateCoordinator], SensorEntity):
    """Implementation of a Hava Durumu sensor."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION
    entity_description: HavaDurumuSensorEntityDescription

    def __init__(
        self,
        coordinator: HavaDurumuDataUpdateCoordinator,
        entry: ConfigEntry,
        description: HavaDurumuSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.data['merkez_id']}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, str(entry.data["merkez_id"]))},
            "name": coordinator.location_name,
            "manufacturer": "MGM",
            "model": "Hava Durumu",
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        
        # Handle alert sensors separately
        if self.entity_description.key == "alert_count":
            alerts = self.coordinator.data.get("alerts", [])
            meteoalarm = self.coordinator.data.get("meteoalarm", [])
            return len(alerts) + len(meteoalarm)
        
        if self.entity_description.key == "alert_details":
            alerts = self.coordinator.data.get("alerts", [])
            meteoalarm = self.coordinator.data.get("meteoalarm", [])
            
            if not alerts and not meteoalarm:
                return "Aktif uyarı yok"
            
            # Format first alert
            if alerts:
                return alerts[0].get("baslik", "Uyarı")
            if meteoalarm:
                return meteoalarm[0].get("aciklama", "Uyarı")
        
        current = self.coordinator.data.get("current")
        if not current:
            return None
        
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(current)
        
        return None
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes for alert sensors."""
        if self.entity_description.key not in ["alert_count", "alert_details"]:
            return {}
        
        if not self.coordinator.data:
            return {}
        
        attrs: dict[str, Any] = {}
        alerts = self.coordinator.data.get("alerts", [])
        meteoalarm = self.coordinator.data.get("meteoalarm", [])
        
        # Format all alerts
        all_alerts = []
        
        for alert in alerts:
            all_alerts.append({
                "type": "MGM Uyarısı",
                "title": alert.get("baslik", ""),
                "description": alert.get("aciklama", ""),
                "date": alert.get("baslangic", ""),
                "event_type": alert.get("hadiseCinsi", ""),
            })
        
        for alert in meteoalarm:
            all_alerts.append({
                "type": "MeteoAlarm",
                "level": alert.get("seviye", ""),
                "area": alert.get("bolge", ""),
                "description": alert.get("aciklama", ""),
            })
        
        if all_alerts:
            attrs["alerts"] = all_alerts
            attrs["total_alerts"] = len(all_alerts)
        
        return attrs
