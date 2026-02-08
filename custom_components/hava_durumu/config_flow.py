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
        self._provinces: list[dict[str, Any]] = []
        self._districts: list[dict[str, Any]] = []
        self._selected_province: dict[str, Any] | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step - province selection."""
        errors: dict[str, str] = {}

        if self._provinces == []:
            try:
                session = async_get_clientsession(self.hass)
                client = MGMApiClient(session)
                self._provinces = await client.get_provinces()
            except MGMApiError:
                errors["base"] = "cannot_connect"
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({}),
                    errors=errors,
                )

        if user_input is not None:
            province_name = user_input[CONF_PROVINCE]
            
            # Find the selected province
            for province in self._provinces:
                if province.get("il") == province_name:
                    self._selected_province = province
                    self._districts = province.get("ilceler", [])
                    break
            
            if self._selected_province:
                return await self.async_step_district()
            
            errors["base"] = "invalid_province"

        # Create province selection dropdown
        province_names = sorted([p.get("il", "") for p in self._provinces])
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PROVINCE): vol.In(province_names),
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
                        province_name = self._selected_province.get("il", "")
                        
                        return self.async_create_entry(
                            title=f"{district_name}, {province_name}",
                            data={
                                CONF_PROVINCE: province_name,
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
        
        province_name = self._selected_province.get("il", "") if self._selected_province else ""
        
        return self.async_show_form(
            step_id="district",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DISTRICT): vol.In(district_names),
                }
            ),
            errors=errors,
            description_placeholders={"province": province_name},
        )
