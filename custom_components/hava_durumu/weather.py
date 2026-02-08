"""Weather platform for Hava Durumu."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.weather import (
    Forecast,
    SingleCoordinatorWeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ATTRIBUTION,
    CONDITION_DESCRIPTIONS,
    CONDITION_MAP,
    DOMAIN,
)
from .coordinator import HavaDurumuDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hava Durumu weather entity from a config entry."""
    coordinator: HavaDurumuDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([HavaDurumuWeather(coordinator, entry)])


class HavaDurumuWeather(SingleCoordinatorWeatherEntity):
    """Implementation of the Hava Durumu weather entity."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_native_pressure_unit = UnitOfPressure.HPA
    _attr_native_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: HavaDurumuDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the weather entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data['merkez_id']}_weather"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, str(entry.data["merkez_id"]))},
            "name": coordinator.location_name,
            "manufacturer": "MGM",
            "model": "Hava Durumu",
        }
        self._attr_supported_features = (
            WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY
        )

    @property
    def _current_data(self) -> dict[str, Any] | None:
        """Get current weather data."""
        if self.coordinator.data:
            return self.coordinator.data.get("current")
        return None

    @property
    def condition(self) -> str | None:
        """Return the current condition."""
        if self._current_data:
            hadise = self._current_data.get("hadiseKodu")
            if hadise:
                return CONDITION_MAP.get(hadise, "cloudy")
        return None

    @property
    def native_temperature(self) -> float | None:
        """Return the temperature."""
        if self._current_data:
            return self._current_data.get("sicaklik")
        return None

    @property
    def native_apparent_temperature(self) -> float | None:
        """Return the apparent temperature."""
        if self._current_data:
            return self._current_data.get("hissedilenSicaklik")
        return None

    @property
    def humidity(self) -> float | None:
        """Return the humidity."""
        if self._current_data:
            return self._current_data.get("nem")
        return None

    @property
    def native_wind_speed(self) -> float | None:
        """Return the wind speed."""
        if self._current_data:
            return self._current_data.get("ruzgarHiz")
        return None

    @property
    def wind_bearing(self) -> float | None:
        """Return the wind bearing."""
        if self._current_data:
            return self._current_data.get("ruzgarYon")
        return None

    @property
    def native_pressure(self) -> float | None:
        """Return the pressure."""
        if self._current_data:
            return self._current_data.get("denizeIndirgenmisBasinc")
        return None

    @property
    def native_visibility(self) -> float | None:
        """Return the visibility in meters."""
        if self._current_data:
            return self._current_data.get("gpisoruss")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        attrs = {}
        if self._current_data:
            hadise = self._current_data.get("hadiseKodu")
            if hadise:
                attrs["condition_text"] = CONDITION_DESCRIPTIONS.get(hadise, hadise)
            
            # Cloud coverage
            if "kappilorta" in self._current_data:
                attrs["cloud_coverage"] = self._current_data.get("kappilorta")
            
            # Precipitation data
            if "ypiagpisipis10Dk" in self._current_data:
                attrs["precipitation_10min"] = self._current_data.get("ypiagpisipis10Dk")
            if "ypiagpisipis1Saat" in self._current_data:
                attrs["precipitation_1h"] = self._current_data.get("ypiagpisipis1Saat")
            if "ypiagpisipis6Saat" in self._current_data:
                attrs["precipitation_6h"] = self._current_data.get("ypiagpisipis6Saat")
            if "ypiagpisipis12Saat" in self._current_data:
                attrs["precipitation_12h"] = self._current_data.get("ypiagpisipis12Saat")
            if "ypiagpisipis24Saat" in self._current_data:
                attrs["precipitation_24h"] = self._current_data.get("ypiagpisipis24Saat")
            
            # Actual pressure
            if "aktuelBasinc" in self._current_data:
                attrs["actual_pressure"] = self._current_data.get("aktuelBasinc")
            
            # Data time
            if "vpieriZamanpi" in self._current_data:
                attrs["data_time"] = self._current_data.get("vpieriZamanpi")
        
        return attrs

    async def async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast."""
        if not self.coordinator.data:
            return None
        
        daily_data = self.coordinator.data.get("daily", [])
        if not daily_data:
            return None
        
        forecasts: list[Forecast] = []
        
        for day in daily_data:
            try:
                # Parse date
                tarih = day.get("tarih")
                if not tarih:
                    continue
                
                hadise = day.get("hadise")
                
                forecast: Forecast = {
                    "datetime": tarih,
                    "condition": CONDITION_MAP.get(hadise, "cloudy") if hadise else None,
                    "native_temperature": day.get("enYuksek"),
                    "native_templow": day.get("enDusuk"),
                }
                
                # Add precipitation probability if available
                if "ypiagpisMiktarpiMax" in day:
                    forecast["precipitation"] = day.get("ypiagpisMiktarpiMax")
                
                forecasts.append(forecast)
            except Exception as err:
                _LOGGER.debug("Error parsing daily forecast: %s", err)
                continue
        
        return forecasts

    async def async_forecast_hourly(self) -> list[Forecast] | None:
        """Return the hourly forecast."""
        if not self.coordinator.data:
            return None
        
        hourly_data = self.coordinator.data.get("hourly", [])
        if not hourly_data:
            return None
        
        forecasts: list[Forecast] = []
        
        for hour in hourly_data:
            try:
                tarih = hour.get("tarih")
                if not tarih:
                    continue
                
                hadise = hour.get("hadise")
                
                forecast: Forecast = {
                    "datetime": tarih,
                    "condition": CONDITION_MAP.get(hadise, "cloudy") if hadise else None,
                    "native_temperature": hour.get("sicaklik"),
                    "humidity": hour.get("nem"),
                    "native_wind_speed": hour.get("ruzgarHizi"),
                    "wind_bearing": hour.get("ruzgarYonu"),
                }
                
                forecasts.append(forecast)
            except Exception as err:
                _LOGGER.debug("Error parsing hourly forecast: %s", err)
                continue
        
        return forecasts
