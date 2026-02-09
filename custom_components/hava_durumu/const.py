"""Constants for the Hava Durumu integration."""
from __future__ import annotations

from homeassistant.components.weather import (
    ATTR_CONDITION_CLEAR_NIGHT,
    ATTR_CONDITION_CLOUDY,
    ATTR_CONDITION_EXCEPTIONAL,
    ATTR_CONDITION_FOG,
    ATTR_CONDITION_HAIL,
    ATTR_CONDITION_LIGHTNING,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_PARTLYCLOUDY,
    ATTR_CONDITION_POURING,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_SUNNY,
    ATTR_CONDITION_WINDY,
)

DOMAIN = "hava_durumu"

# API Configuration
API_BASE_URL = "https://servis.mgm.gov.tr/mobile"
API_AUTH_TOKEN = "0jTmRuHuhcOHntmuzkmJS/95CFj72gVR2+9wRYwta+A="
API_USER_AGENT = "Meteoroloji/6.1.2 (com.mgm.Hava-Durumu; build:1; iOS 26.2.1) Alamofire/4.7.3"

# Update interval in seconds (30 minutes)
UPDATE_INTERVAL = 1800

# API Endpoints
ENDPOINT_PROVINCES = "/merkezler/iller"
ENDPOINT_SEARCH = "/merkezler"
ENDPOINT_CURRENT = "/sondurumlar"
ENDPOINT_HOURLY = "/tahminler/saatlik"
ENDPOINT_DAILY = "/tahminler/gunluk"
ENDPOINT_ALERTS = "/alarmlar"
ENDPOINT_ALERT_DETAIL = "/alarmlar/detay"
ENDPOINT_METEOALARM_TODAY = "/meteoalarm/today"
ENDPOINT_METEOALARM_TOMORROW = "/meteoalarm/tomorrow"

# Configuration keys
CONF_PROVINCE = "province"
CONF_DISTRICT = "district"
CONF_MERKEZ_ID = "merkez_id"
CONF_STATION_ID = "station_id"
CONF_ENABLE_NOTIFICATIONS = "enable_notifications"

# Platforms
PLATFORMS = ["weather", "sensor", "binary_sensor"]

# Weather condition code mapping (MGM hadiseKodu -> Turkish description)
CONDITION_DESCRIPTIONS = {
    "A": "Açık",
    "AB": "Az Bulutlu",
    "PB": "Parçalı Bulutlu",
    "CB": "Çok Bulutlu",
    "HY": "Hafif Yağmurlu",
    "Y": "Yağmurlu",
    "KY": "Kuvvetli Yağmurlu",
    "MSY": "Yer Yer Sağanak Yağışlı",
    "HSY": "Hafif Sağanak Yağışlı",
    "SY": "Sağanak Yağışlı",
    "KSY": "Kuvvetli Sağanak Yağışlı",
    "TS": "Gökgürültülü",
    "GSY": "Gökgürültülü Sağanak Yağışlı",
    "KGY": "Kuvvetli Gökgürültülü Sağanak Yağışlı",
    "KKY": "Karla Karışık Yağmurlu",
    "HKY": "Hafif Kar Yağışlı",
    "K": "Kar Yağışlı",
    "YKY": "Yoğun Kar Yağışlı",
    "DY": "Dolu",
    "DMN": "Dumanlı",
    "PUS": "Puslu",
    "SIS": "Sisli",
    "R": "Rüzgarlı",
    "KF": "Toz veya Kum Fırtınası",
    "GKR": "Güneyli Kuvvetli Rüzgar",
    "KKR": "Kuzeyli Kuvvetli Rüzgar",
    "HHY": "Yağışlı",
    "SCK": "Sıcak",
    "SGK": "Soğuk",
}

# MGM condition code to Home Assistant condition mapping
CONDITION_MAP = {
    "A": ATTR_CONDITION_SUNNY,
    "AB": ATTR_CONDITION_PARTLYCLOUDY,
    "PB": ATTR_CONDITION_PARTLYCLOUDY,
    "CB": ATTR_CONDITION_CLOUDY,
    "HY": ATTR_CONDITION_RAINY,
    "Y": ATTR_CONDITION_RAINY,
    "KY": ATTR_CONDITION_POURING,
    "MSY": ATTR_CONDITION_RAINY,
    "HSY": ATTR_CONDITION_RAINY,
    "SY": ATTR_CONDITION_POURING,
    "KSY": ATTR_CONDITION_POURING,
    "TS": ATTR_CONDITION_LIGHTNING,
    "GSY": ATTR_CONDITION_LIGHTNING_RAINY,
    "KGY": ATTR_CONDITION_LIGHTNING_RAINY,
    "KKY": ATTR_CONDITION_SNOWY_RAINY,
    "HKY": ATTR_CONDITION_SNOWY,
    "K": ATTR_CONDITION_SNOWY,
    "YKY": ATTR_CONDITION_SNOWY,
    "DY": ATTR_CONDITION_HAIL,
    "DMN": ATTR_CONDITION_FOG,
    "PUS": ATTR_CONDITION_FOG,
    "SIS": ATTR_CONDITION_FOG,
    "R": ATTR_CONDITION_WINDY,
    "KF": ATTR_CONDITION_EXCEPTIONAL,
    "GKR": ATTR_CONDITION_WINDY,
    "KKR": ATTR_CONDITION_WINDY,
    "HHY": ATTR_CONDITION_RAINY,
    "SCK": ATTR_CONDITION_SUNNY,
    "SGK": ATTR_CONDITION_CLOUDY,
}

# Wind direction mapping (degrees to cardinal direction)
WIND_DIRECTIONS = {
    (0, 22.5): "K",      # North
    (22.5, 67.5): "KD",  # Northeast
    (67.5, 112.5): "D",  # East
    (112.5, 157.5): "GD", # Southeast
    (157.5, 202.5): "G",  # South
    (202.5, 247.5): "GB", # Southwest
    (247.5, 292.5): "B",  # West
    (292.5, 337.5): "KB", # Northwest
    (337.5, 360): "K",    # North
}

# Wind direction full names in Turkish
WIND_DIRECTION_NAMES = {
    "K": "Kuzey",
    "KD": "Kuzeydoğu",
    "D": "Doğu",
    "GD": "Güneydoğu",
    "G": "Güney",
    "GB": "Güneybatı",
    "B": "Batı",
    "KB": "Kuzeybatı",
}

# Sensor types
SENSOR_TYPES = {
    "humidity": {
        "name": "Nem",
        "device_class": "humidity",
        "unit": "%",
        "icon": "mdi:water-percent",
    },
    "wind_speed": {
        "name": "Rüzgar Hızı",
        "device_class": "wind_speed",
        "unit": "km/h",
        "icon": "mdi:weather-windy",
    },
    "wind_bearing": {
        "name": "Rüzgar Yönü",
        "device_class": None,
        "unit": "°",
        "icon": "mdi:compass",
    },
    "pressure": {
        "name": "Basınç",
        "device_class": "pressure",
        "unit": "hPa",
        "icon": "mdi:gauge",
    },
    "visibility": {
        "name": "Görüş Mesafesi",
        "device_class": "distance",
        "unit": "m",
        "icon": "mdi:eye",
    },
    "precipitation_1h": {
        "name": "Yağış (1 Saat)",
        "device_class": "precipitation",
        "unit": "mm",
        "icon": "mdi:weather-rainy",
    },
    "precipitation_24h": {
        "name": "Yağış (24 Saat)",
        "device_class": "precipitation",
        "unit": "mm",
        "icon": "mdi:weather-rainy",
    },
    "cloud_coverage": {
        "name": "Bulutluluk",
        "device_class": None,
        "unit": "okta",
        "icon": "mdi:cloud",
    },
    "apparent_temperature": {
        "name": "Hissedilen Sıcaklık",
        "device_class": "temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
    },
    "condition_text": {
        "name": "Hava Durumu",
        "device_class": None,
        "unit": None,
        "icon": "mdi:weather-partly-cloudy",
    },
}

# Attribution
ATTRIBUTION = "Veriler: T.C. Çevre, Şehircilik ve İklim Değişikliği Bakanlığı Meteoroloji Genel Müdürlüğü"
