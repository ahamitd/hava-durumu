"""API client for MGM (Turkish Meteorological Service)."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

import aiohttp

from .const import (
    API_AUTH_TOKEN,
    API_BASE_URL,
    API_USER_AGENT,
    ENDPOINT_ALERTS,
    ENDPOINT_ALERT_DETAIL,
    ENDPOINT_CURRENT,
    ENDPOINT_DAILY,
    ENDPOINT_HOURLY,
    ENDPOINT_METEOALARM_TODAY,
    ENDPOINT_METEOALARM_TOMORROW,
    ENDPOINT_PROVINCES,
    ENDPOINT_SEARCH,
)

_LOGGER = logging.getLogger(__name__)


class MGMApiError(Exception):
    """Exception for MGM API errors."""

    pass


class MGMApiClient:
    """MGM API Client."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session
        self._headers = {
            "Authorization-token-ios": API_AUTH_TOKEN,
            "Accept": "*/*",
            "User-Agent": API_USER_AGENT,
            "Accept-Language": "tr-TR;q=1.0, en-TR;q=0.9",
            "Accept-Encoding": "gzip",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }

    async def _request(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> Any:
        """Make an API request."""
        url = f"{API_BASE_URL}{endpoint}"
        
        try:
            async with self._session.get(
                url, headers=self._headers, params=params, timeout=30
            ) as response:
                if response.status == 304:
                    _LOGGER.debug("API returned 304 for %s", url)
                    return None
                    
                if response.status != 200:
                    _LOGGER.error(
                        "API request failed: %s, status: %s",
                        url,
                        response.status,
                    )
                    raise MGMApiError(f"API request failed with status {response.status}")
                
                data = await response.json()
                _LOGGER.debug("API response for %s: %s", url, "success")
                return data
                
        except asyncio.TimeoutError as err:
            _LOGGER.error("API request timeout: %s", url)
            raise MGMApiError("API request timeout") from err
        except aiohttp.ClientError as err:
            _LOGGER.error("API request error: %s - %s", url, str(err))
            raise MGMApiError(f"API request error: {str(err)}") from err

    async def get_provinces(self) -> list[dict[str, Any]]:
        """Get list of all provinces."""
        result = await self._request(ENDPOINT_PROVINCES)
        if result is None:
            return []
        return result

    async def search_locations(self, query: str, limit: int = 15) -> list[dict[str, Any]]:
        """Search for locations by name."""
        result = await self._request(
            ENDPOINT_SEARCH,
            params={"sorgu": query, "limit": limit}
        )
        if result is None:
            return []
        return result

    async def get_current_weather(self, merkez_id: int) -> dict[str, Any] | None:
        """Get current weather data for a location."""
        result = await self._request(
            ENDPOINT_CURRENT,
            params={"merkezid": merkez_id}
        )
        if result is None or not result:
            return None
        # API returns a list, we need the first item
        return result[0] if isinstance(result, list) else result

    async def get_hourly_forecast(
        self, merkez_id: int, datetime_str: str | None = None
    ) -> list[dict[str, Any]]:
        """Get hourly forecast data."""
        if datetime_str is None:
            datetime_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        result = await self._request(
            ENDPOINT_HOURLY,
            params={"merkezid": merkez_id, "datetime": datetime_str}
        )
        if result is None or not result:
            return []
        
        # Extract forecast list from response
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("tahmin", [])
        return []

    async def get_daily_forecast(self, merkez_id: int) -> list[dict[str, Any]]:
        """Get daily forecast data (5 days)."""
        result = await self._request(
            ENDPOINT_DAILY,
            params={"istno": merkez_id}
        )
        if result is None or not result:
            return []
        
        # API returns data in format: enDusukGun0, enYuksekGun0, etc.
        # We need to transform this into a list of daily forecasts
        if isinstance(result, list) and len(result) > 0:
            raw_data = result[0]
            forecasts = []
            
            # Process Gun0 through Gun5 (6 days total)
            for i in range(6):
                day_data = {
                    "tarih": raw_data.get(f"tarihGun{i}"),
                    "enDusuk": raw_data.get(f"enDusukGun{i}"),
                    "enYuksek": raw_data.get(f"enYuksekGun{i}"),
                    "hadise": raw_data.get(f"hadiseGun{i}"),
                    "ruzgarHizi": raw_data.get(f"ruzgarHizGun{i}"),
                    "ruzgarYonu": raw_data.get(f"ruzgarYonGun{i}"),
                    "enDusukNem": raw_data.get(f"enDusukNemGun{i}"),
                    "enYuksekNem": raw_data.get(f"enYuksekNemGun{i}"),
                }
                
                # Only add if we have valid data
                if day_data["tarih"]:
                    forecasts.append(day_data)
            
            return forecasts
        
        return []

    async def get_alerts(self) -> list[dict[str, Any]]:
        """Get list of active weather alerts."""
        result = await self._request(ENDPOINT_ALERTS)
        if result is None:
            return []
        return result

    async def get_alert_detail(self, alarm_no: str) -> dict[str, Any] | None:
        """Get details of a specific alert."""
        result = await self._request(
            ENDPOINT_ALERT_DETAIL,
            params={"alarmno": alarm_no}
        )
        return result

    async def get_meteoalarm_today(self) -> list[dict[str, Any]]:
        """Get today's meteo alarms."""
        result = await self._request(ENDPOINT_METEOALARM_TODAY)
        if result is None:
            return []
        return result

    async def get_meteoalarm_tomorrow(self) -> list[dict[str, Any]]:
        """Get tomorrow's meteo alarms."""
        result = await self._request(ENDPOINT_METEOALARM_TOMORROW)
        if result is None:
            return []
        return result

    async def get_all_data(self, merkez_id: int) -> dict[str, Any]:
        """Get all weather data for a location."""
        try:
            current, hourly, daily, alerts, meteoalarm_today = await asyncio.gather(
                self.get_current_weather(merkez_id),
                self.get_hourly_forecast(merkez_id),
                self.get_daily_forecast(merkez_id),
                self.get_alerts(),
                self.get_meteoalarm_today(),
                return_exceptions=True,
            )
            
            # Handle exceptions in gathered results
            if isinstance(current, Exception):
                _LOGGER.warning("Failed to get current weather: %s", current)
                current = None
            if isinstance(hourly, Exception):
                _LOGGER.warning("Failed to get hourly forecast: %s", hourly)
                hourly = []
            if isinstance(daily, Exception):
                _LOGGER.warning("Failed to get daily forecast: %s", daily)
                daily = []
            if isinstance(alerts, Exception):
                _LOGGER.warning("Failed to get alerts: %s", alerts)
                alerts = []
            if isinstance(meteoalarm_today, Exception):
                _LOGGER.warning("Failed to get meteoalarm: %s", meteoalarm_today)
                meteoalarm_today = []

            return {
                "current": current,
                "hourly": hourly,
                "daily": daily,
                "alerts": alerts,
                "meteoalarm": meteoalarm_today,
            }
        except Exception as err:
            _LOGGER.error("Failed to get all data: %s", err)
            raise MGMApiError(f"Failed to get all data: {str(err)}") from err
