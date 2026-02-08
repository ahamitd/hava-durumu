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


def get_wind_direction_text(degrees: float | None) -> str | None:
    """Convert wind bearing degrees to Turkish cardinal direction.
    
    Args:
        degrees: Wind bearing in degrees (0-360)
        
    Returns:
        Turkish direction abbreviation (K, KB, D, GD, G, GB, B, KB) or None
    """
    if degrees is None:
        return None
    
    from .const import WIND_DIRECTIONS
    
    # Normalize degrees to 0-360 range
    degrees = degrees % 360
    
    # Find matching direction range
    for (min_deg, max_deg), direction in WIND_DIRECTIONS.items():
        if min_deg <= degrees < max_deg:
            return direction
    
    return None


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
        value_fn=lambda data: data.get("nem") if data.get("nem") is not None and data.get("nem") != -9999 else None,
    ),
    HavaDurumuSensorEntityDescription(
        key="wind_speed",
        translation_key="wind_speed",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("ruzgarHiz") if data.get("ruzgarHiz") is not None and data.get("ruzgarHiz") != -9999 else None,
    ),
    HavaDurumuSensorEntityDescription(
        key="wind_bearing",
        translation_key="wind_bearing",
        icon="mdi:compass",
        value_fn=lambda data: get_wind_direction_text(data.get("ruzgarYon")),
    ),
    HavaDurumuSensorEntityDescription(
        key="pressure",
        translation_key="pressure",
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("denizeIndirgenmisBasinc") if data.get("denizeIndirgenmisBasinc") is not None and data.get("denizeIndirgenmisBasinc") != -9999 else None,
    ),
    HavaDurumuSensorEntityDescription(
        key="visibility",
        translation_key="visibility",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("gorus") if data.get("gorus") is not None and data.get("gorus") != -9999 and data.get("gorus") > 0 else None,
    ),
    HavaDurumuSensorEntityDescription(
        key="precipitation_current",
        translation_key="precipitation_current",
        native_unit_of_measurement="mm",
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:weather-rainy",
        value_fn=lambda data: data.get("yagis00Now") if data.get("yagis00Now") and data.get("yagis00Now") != -9999 else None,
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
        value_fn=lambda data: data.get("kapalilik") if data.get("kapalilik") is not None and data.get("kapalilik") != -9999 else None,
    ),
    HavaDurumuSensorEntityDescription(
        key="apparent_temperature",
        translation_key="apparent_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("hissedilenSicaklik") if data.get("hissedilenSicaklik") is not None and data.get("hissedilenSicaklik") != -9999 else None,
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
    HavaDurumuSensorEntityDescription(
        key="forecast_today",
        translation_key="forecast_today",
        icon="mdi:calendar-today",
        value_fn=None,  # Will be handled separately
    ),
    HavaDurumuSensorEntityDescription(
        key="forecast_tomorrow",
        translation_key="forecast_tomorrow",
        icon="mdi:calendar-tomorrow",
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
        
        # Handle forecast sensors separately
        if self.entity_description.key == "forecast_today":
            daily = self.coordinator.data.get("daily", [])
            if daily and len(daily) > 0:
                today = daily[0]
                hadise_code = today.get("hadise", "")
                return CONDITION_DESCRIPTIONS.get(hadise_code, hadise_code)
            return None
        
        if self.entity_description.key == "forecast_tomorrow":
            daily = self.coordinator.data.get("daily", [])
            if daily and len(daily) > 1:
                tomorrow = daily[1]
                hadise_code = tomorrow.get("hadise", "")
                return CONDITION_DESCRIPTIONS.get(hadise_code, hadise_code)
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
        """Return additional state attributes for special sensors."""
        if self.entity_description.key not in ["alert_count", "alert_details", "wind_bearing", "forecast_today", "forecast_tomorrow"]:
            return {}
        
        if not self.coordinator.data:
            return {}
        
        # Handle forecast attributes
        if self.entity_description.key == "forecast_today":
            daily = self.coordinator.data.get("daily", [])
            if daily and len(daily) > 0:
                today = daily[0]
                return {
                    "date": today.get("tarih"),
                    "min_temp": today.get("enDusuk"),
                    "max_temp": today.get("enYuksek"),
                    "condition_code": today.get("hadise"),
                }
            return {}
        
        if self.entity_description.key == "forecast_tomorrow":
            daily = self.coordinator.data.get("daily", [])
            if daily and len(daily) > 1:
                tomorrow = daily[1]
                return {
                    "date": tomorrow.get("tarih"),
                    "min_temp": tomorrow.get("enDusuk"),
                    "max_temp": tomorrow.get("enYuksek"),
                    "condition_code": tomorrow.get("hadise"),
                }
            return {}
        
        # Handle wind bearing attributes
        if self.entity_description.key == "wind_bearing":
            from .const import WIND_DIRECTION_NAMES
            
            current = self.coordinator.data.get("current")
            if not current:
                return {}
            
            degrees = current.get("ruzgarYon")
            if degrees is None:
                return {}
            
            attrs: dict[str, Any] = {
                "degrees": degrees,
            }
            
            # Add full direction name
            direction_abbr = get_wind_direction_text(degrees)
            if direction_abbr:
                attrs["direction_full"] = WIND_DIRECTION_NAMES.get(direction_abbr, "")
            
            return attrs
        
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
