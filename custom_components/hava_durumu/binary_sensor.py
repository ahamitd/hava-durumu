"""Binary sensor platform for Hava Durumu alerts."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import HavaDurumuDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hava Durumu binary sensor entities from a config entry."""
    coordinator: HavaDurumuDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([HavaDurumuAlertSensor(coordinator, entry)])


class HavaDurumuAlertSensor(
    CoordinatorEntity[HavaDurumuDataUpdateCoordinator], BinarySensorEntity
):
    """Binary sensor for active weather alerts."""

    _attr_has_entity_name = True
    _attr_translation_key = "weather_alert"
    _attr_attribution = ATTRIBUTION
    _previous_alert_count: int = 0

    def __init__(
        self,
        coordinator: HavaDurumuDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data['merkez_id']}_alert"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, str(entry.data["merkez_id"]))},
            "name": coordinator.location_name,
            "manufacturer": "MGM",
            "model": "Hava Durumu",
        }
        self._entry = entry

    @property
    def is_on(self) -> bool:
        """Return true if there are active alerts."""
        if not self.coordinator.data:
            return False
        
        alerts = self.coordinator.data.get("alerts", [])
        meteoalarm = self.coordinator.data.get("meteoalarm", [])
        
        return len(alerts) > 0 or len(meteoalarm) > 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        attrs: dict[str, Any] = {}
        
        if not self.coordinator.data:
            return attrs
        
        alerts = self.coordinator.data.get("alerts", [])
        meteoalarm = self.coordinator.data.get("meteoalarm", [])
        
        attrs["alert_count"] = len(alerts) + len(meteoalarm)
        
        # Format alerts for display
        all_alerts = []
        
        for alert in alerts:
            all_alerts.append({
                "type": "MGM Uyarısı",
                "title": alert.get("baslik", ""),
                "description": alert.get("aciklama", ""),
                "date": alert.get("tarih", ""),
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
            attrs["last_alert"] = all_alerts[0].get("title") or all_alerts[0].get("description", "")
        
        return attrs

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        super()._handle_coordinator_update()
        
        # Check for new alerts and create notifications
        if self.coordinator.data:
            current_alert_count = len(self.coordinator.data.get("alerts", [])) + len(
                self.coordinator.data.get("meteoalarm", [])
            )
            
            # If new alerts appeared, create a notification
            if current_alert_count > self._previous_alert_count and current_alert_count > 0:
                self._create_alert_notification()
            
            self._previous_alert_count = current_alert_count

    def _create_alert_notification(self) -> None:
        """Create a persistent notification for new alerts."""
        alerts = self.coordinator.data.get("alerts", [])
        meteoalarm = self.coordinator.data.get("meteoalarm", [])
        
        message_parts = []
        
        for alert in alerts[:3]:  # Limit to first 3 alerts
            title = alert.get("baslik", "")
            desc = alert.get("aciklama", "")
            if title or desc:
                message_parts.append(f"⚠️ **{title}**\n{desc}")
        
        for alert in meteoalarm[:3]:
            level = alert.get("seviye", "")
            area = alert.get("bolge", "")
            desc = alert.get("aciklama", "")
            message_parts.append(f"🚨 **MeteoAlarm - {level}** ({area})\n{desc}")
        
        if message_parts:
            message = "\n\n".join(message_parts)
            
            self.hass.async_create_task(
                self.hass.services.async_call(
                    "persistent_notification",
                    "create",
                    {
                        "title": f"🌩️ Hava Durumu Uyarısı - {self.coordinator.location_name}",
                        "message": message,
                        "notification_id": f"hava_durumu_alert_{self._entry.data['merkez_id']}",
                    },
                )
            )
