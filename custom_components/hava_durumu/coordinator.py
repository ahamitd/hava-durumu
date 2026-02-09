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

        # Get update interval from options, default to 30 minutes
        update_interval = int(entry.options.get("update_interval", UPDATE_INTERVAL))

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from MGM API."""
        _LOGGER.debug(
            "Fetching MGM weather data for %s (interval: %s)",
            self.location_name,
            self.update_interval,
        )
        try:
            new_data = await self.api.get_all_data(self.merkez_id)
            
            # If we already have data and the new current data is None (304), 
            # keep the old data for current weather to avoid "unknown" state
            if self.data and new_data.get("current") is None:
                _LOGGER.debug("API returned no update for current weather, keeping old data")
                new_data["current"] = self.data.get("current")
            
            if new_data.get("current") is None:
                _LOGGER.warning("No current weather data received for %s", self.location_name)
            
            return new_data
            
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
