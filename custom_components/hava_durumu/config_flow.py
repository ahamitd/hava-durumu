"""Config flow for Hava Durumu integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MGMApiClient, MGMApiError
from .const import CONF_DISTRICT, CONF_MERKEZ_ID, CONF_PROVINCE, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def validate_location(
    hass: HomeAssistant, merkez_id: int
) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    client = MGMApiClient(session)
    
    try:
        current = await client.get_current_weather(merkez_id)
        if current is None:
            raise ValueError("No data for this location")
        return {"title": f"Hava Durumu"}
    except MGMApiError as err:
        _LOGGER.error("API Error during validation: %s", err)
        raise


class HavaDurumuConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hava Durumu."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._provinces: list[str] = []
        self._districts: list[dict[str, Any]] = []
        self._selected_province: str | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step - province selection."""
        errors: dict[str, str] = {}

        if not self._provinces:
            try:
                session = async_get_clientsession(self.hass)
                client = MGMApiClient(session)
                # Get only province centers for initial list
                all_locations = await client.get_provinces()
                
                # Extract unique provinces
                provinces_set = set()
                for location in all_locations:
                    il = location.get("il", "")
                    if il:
                        provinces_set.add(il)
                
                self._provinces = sorted(list(provinces_set))
            except MGMApiError:
                errors["base"] = "cannot_connect"
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({}),
                    errors=errors,
                )

        if user_input is not None:
            province_name = user_input[CONF_PROVINCE]
            
            if province_name in self._provinces:
                self._selected_province = province_name
                # Fetch all districts for the selected province
                try:
                    session = async_get_clientsession(self.hass)
                    client = MGMApiClient(session)
                    self._districts = await client.search_locations(province_name, limit=100)
                except MGMApiError:
                    errors["base"] = "cannot_connect"
                    return self.async_show_form(
                        step_id="user",
                        data_schema=vol.Schema({
                            vol.Required(CONF_PROVINCE): vol.In(self._provinces),
                        }),
                        errors=errors,
                    )
                
                return await self.async_step_district()
            
            errors["base"] = "invalid_province"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PROVINCE): vol.In(self._provinces),
                }
            ),
            errors=errors,
        )

    async def async_step_district(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the second step - district selection."""
        errors: dict[str, str] = {}

        if user_input is not None:
            district_name = user_input[CONF_DISTRICT]
            
            # Find the selected district
            selected_district = None
            for district in self._districts:
                if district.get("ilce") == district_name:
                    selected_district = district
                    break
            
            if selected_district:
                merkez_id = selected_district.get("merkezId")
                
                if merkez_id:
                    # Check for existing entry with same merkez_id
                    await self.async_set_unique_id(f"{merkez_id}")
                    self._abort_if_unique_id_configured()
                    
                    try:
                        await validate_location(self.hass, merkez_id)
                    except (MGMApiError, ValueError):
                        errors["base"] = "cannot_connect"
                    else:
                        return self.async_create_entry(
                            title=f"{district_name}, {self._selected_province}",
                            data={
                                CONF_PROVINCE: self._selected_province,
                                CONF_DISTRICT: district_name,
                                CONF_MERKEZ_ID: merkez_id,
                            },
                        )
                else:
                    errors["base"] = "invalid_district"
            else:
                errors["base"] = "invalid_district"

        # Create district selection dropdown
        district_names = sorted([d.get("ilce", "") for d in self._districts])
        
        return self.async_show_form(
            step_id="district",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DISTRICT): vol.In(district_names),
                }
            ),
            errors=errors,
            description_placeholders={"province": self._selected_province},
        )

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return HavaDurumuOptionsFlow(config_entry)


class HavaDurumuOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Hava Durumu."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "update_interval",
                        default=int(self._config_entry.options.get("update_interval", 1800)),
                    ): vol.In(
                        {
                            300: "5 dakika",
                            600: "10 dakika",
                            900: "15 dakika",
                            1800: "30 dakika",
                            3600: "60 dakika",
                        }
                    ),
                    vol.Required(
                        "enable_notifications",
                        default=self._config_entry.options.get("enable_notifications", True),
                    ): bool,
                }
            ),
        )
