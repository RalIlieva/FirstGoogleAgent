# minimal city time + weather agent using ADK function tools
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from google.adk.agents import Agent


def get_weather(city: str) -> dict:
    """Fetch current weather via Open-Meteo (no API key)."""
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en"},
            timeout=10,
        ).json()
        if not geo.get("results"):
            return {"status": "error", "error_message": f"Couldn't find '{city}'."}
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        w = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True},
            timeout=10,
        ).json()
        cw = w.get("current_weather")
        if not cw:
            return {"status": "error", "error_message": "No weather data."}
        desc = f"{cw['temperature']}°C, wind {cw['windspeed']} km/h"
        return {"status": "success", "report": f"Weather in {city}: {desc}"}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


def get_current_time(city: str) -> dict:
    """Get local time using Open-Meteo’s timezone from geocoding."""
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en"},
            timeout=10,
        ).json()
        if not geo.get("results"):
            return {"status": "error", "error_message": f"Couldn't find '{city}'."}
        tz = geo["results"][0]["timezone"]
        now = datetime.now(ZoneInfo(tz))
        return {"status": "success", "report": now.strftime("Local time in %s: %Y-%m-%d %H:%M:%S %Z") % city}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


root_agent = Agent(
    name="mini_travel_helper",
    model="gemini-2.0-flash",
    description="Answers questions about current weather and local time for a city.",
    instruction="Be concise. Use tools only when necessary.",
    tools=[get_weather, get_current_time],
)
