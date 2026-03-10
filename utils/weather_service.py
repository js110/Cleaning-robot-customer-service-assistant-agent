import json
from urllib.parse import urlencode
from urllib.request import urlopen

GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_API = "https://api.open-meteo.com/v1/forecast"
IP_GEOLOCATION_APIS = (
    "https://ipwho.is/",
    "https://ipapi.co/json/",
)

WEATHER_CODE_MAP = {
    0: "晴",
    1: "大体晴",
    2: "局部多云",
    3: "阴",
    45: "雾",
    48: "冻雾",
    51: "小毛毛雨",
    53: "毛毛雨",
    55: "大毛毛雨",
    56: "冻毛毛雨",
    57: "强冻毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    66: "冻雨",
    67: "强冻雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "冰粒",
    80: "阵雨",
    81: "强阵雨",
    82: "暴雨阵雨",
    85: "阵雪",
    86: "强阵雪",
    95: "雷暴",
    96: "雷暴伴小冰雹",
    99: "雷暴伴强冰雹",
}


def fetch_json(url: str, params: dict | None = None) -> dict:
    full_url = url
    if params:
        full_url = f"{url}?{urlencode(params)}"
    with urlopen(full_url, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def weather_code_to_text(code: int | None) -> str:
    if code is None:
        return "未知"
    return WEATHER_CODE_MAP.get(code, f"未知天气({code})")


def resolve_city(city: str) -> dict:
    data = fetch_json(
        GEOCODING_API,
        {
            "name": city,
            "count": 1,
            "language": "zh",
            "format": "json",
        },
    )
    results = data.get("results") or []
    if not results:
        raise ValueError(f"没有找到城市“{city}”")
    return results[0]


def get_user_city() -> str:
    last_error = None
    for api in IP_GEOLOCATION_APIS:
        try:
            data = fetch_json(api)
            if api.endswith("ipwho.is/"):
                if not data.get("success", False):
                    raise ValueError(data.get("message") or "IP 定位失败")
                city = data.get("city")
                region = data.get("region")
                country = data.get("country")
            else:
                if data.get("error"):
                    raise ValueError(data.get("reason") or "IP 定位失败")
                city = data.get("city")
                region = data.get("region")
                country = data.get("country_name")

            parts = [part for part in [country, region, city] if part]
            if not parts:
                raise ValueError("没有返回可用的位置字段")
            return parts[-1]
        except Exception as exc:
            last_error = exc
            continue

    raise RuntimeError(f"获取用户位置失败: {last_error}")


def fetch_weather(city: str) -> str:
    location = resolve_city(city)
    forecast = fetch_json(
        FORECAST_API,
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "forecast_days": 1,
            "timezone": "auto",
        },
    )

    current = forecast.get("current", {})
    daily = forecast.get("daily", {})
    city_name = location.get("name", city)
    admin1 = location.get("admin1")
    country = location.get("country")
    region = " ".join(part for part in [country, admin1, city_name] if part)

    current_desc = weather_code_to_text(current.get("weather_code"))
    daily_codes = daily.get("weather_code") or [None]
    daily_desc = weather_code_to_text(daily_codes[0])
    temp_max = (daily.get("temperature_2m_max") or [None])[0]
    temp_min = (daily.get("temperature_2m_min") or [None])[0]
    rain_prob = (daily.get("precipitation_probability_max") or [None])[0]

    parts = [
        f"{region}当前天气{current_desc}",
        f"气温{current.get('temperature_2m')}°C",
        f"湿度{current.get('relative_humidity_2m')}%",
        f"风速{current.get('wind_speed_10m')}km/h",
        f"今日日间预报{daily_desc}",
    ]
    if temp_min is not None and temp_max is not None:
        parts.append(f"最低{temp_min}°C，最高{temp_max}°C")
    if rain_prob is not None:
        parts.append(f"降水概率{rain_prob}%")
    return "，".join(parts) + "。"
