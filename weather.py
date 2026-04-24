import os
import sys
import requests
from typing import Optional, Dict, Any

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
TIMEOUT = 10

def get_coordinate(city: str) -> Optional[Dict[str, Any]]:
    geo_url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "limit": 1,
        "appid": API_KEY
    }
    try:
        resp = requests.get(geo_url, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            print(f"未找到该城市: {city}, 请检查拼写")
            return None

        first = data[0]
        return {
            "lat": first["lat"],
            "lon": first["lon"],
            "name": first.get("name"),
            "country": first.get("country", ""),
        }
    except requests.exceptions.Timeout:
        print("地理编码请求超时, 请检查网络或稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"地理编码请求失败: {e}")
    except (KeyError, IndexError, TypeError) as e:
        print(f"解析地理位置数据出错: {e}")
    return None


def get_weather_data(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_cn"
    }
    try:
        resp = requests.get(weather_url, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        print("天气数据请求超时, 请稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"天气数据请求失败: {e}")
    except ValueError as e:
        print(f"响应数据格式异常: {e}")
    return None


def display_weather(location: Dict[str, Any], weather: Dict[str, Any]) -> None:
    main = weather.get("main", {})
    wind = weather.get("wind", {})
    weather_list = weather.get("weather")
    weather_desc = weather_list[0] if weather_list else {}

    temp = main.get("temp", "N/A")
    feels_like = main.get("feels_like", "N/A")
    humidity = main.get("humidity", "N/A")
    desc = weather_desc.get("description", "未知")
    wind_speed = wind.get("speed", "N/A")

    print("\n" + "=" * 45)
    print(f"{location['name']}, {location['country']}")
    print(f"温度: {temp}℃ (体感{feels_like}℃)")
    print(f"天气: {desc}")
    print(f"湿度: {humidity}%")
    print(f"风速: {wind_speed}m/s")
    print("=" * 45)


def query_weather(city: str) -> None:
    if not API_KEY:
        print("请设置环境变量 OPENWEATHER_API_KEY")
        sys.exit(1)

    location = get_coordinate(city)
    if not location:
        return

    weather = get_weather_data(location["lat"], location["lon"])
    if not weather:
        return

    display_weather(location, weather)


def main():
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
    else:
        city = input("请输入城市名: ").strip()

    if not city:
        print("城市名字不能为空")
        sys.exit(1)

    query_weather(city)


if __name__ == "__main__":
    main()
