"""Button platform for Hava Durumu."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
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
    """Set up Hava Durumu button entities from a config entry."""
    coordinator: HavaDurumuDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([HavaDurumuRefreshButton(coordinator, entry)])


class HavaDurumuRefreshButton(
    CoordinatorEntity[HavaDurumuDataUpdateCoordinator], ButtonEntity
):
    """Button to manually refresh weather data."""

    _attr_has_entity_name = True
    _attr_translation_key = "refresh"
    _attr_attribution = ATTRIBUTION
    _attr_icon = "mdi:refresh"

    def __init__(
        self,
        coordinator: HavaDurumuDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data['merkez_id']}_refresh"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, str(entry.data["merkez_id"]))},
            "name": coordinator.location_name,
            "manufacturer": "MGM",
            "model": "Hava Durumu",
        }

    async def async_press(self) -> None:
        """Handle the button press - refresh all data."""
        _LOGGER.debug("Manuel güncelleme başlatıldı")
        await self.coordinator.async_request_refresh()
