"""Data update coordinator for Hava Durumu."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MGMApiClient, MGMApiError
from .const import CONF_MERKEZ_ID, DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class HavaDurumuDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Hava Durumu data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.merkez_id = entry.data[CONF_MERKEZ_ID]
        self.province = entry.data.get("province", "")
        self.district = entry.data.get("district", "")
        
        session = async_get_clientsession(hass)
        self.api = MGMApiClient(session)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from MGM API."""
        try:
            data = await self.api.get_all_data(self.merkez_id)
            
            if data.get("current") is None:
                _LOGGER.warning("No current weather data received")
            
            return data
            
        except MGMApiError as err:
            raise UpdateFailed(f"Error fetching MGM data: {err}") from err
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching MGM data")
            raise UpdateFailed(f"Unexpected error: {err}") from err

    @property
    def location_name(self) -> str:
        """Return the location name."""
        if self.district:
            return f"{self.district}, {self.province}"
        return self.province
