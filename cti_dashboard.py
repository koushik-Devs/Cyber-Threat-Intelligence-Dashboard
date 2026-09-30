import os
import requests
import pandas as pd

API_KEY = os.environ.get("OTX_API_KEY", "").strip()
BASE_URL = "https://otx.alienvault.com/api/v1"


def get_recent_pulses(limit=50):
    if not API_KEY:
        raise RuntimeError("Set OTX_API_KEY in the environment before fetching pulses.")
    if not isinstance(limit, int) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer between 1 and 100")

    response = requests.get(
        f"{BASE_URL}/pulses/subscribed",
        headers={"X-OTX-API-KEY": API_KEY},
        params={"limit": limit},
        timeout=(5, 30),
    )
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results")
    if not isinstance(results, list):
        raise ValueError("Unexpected OTX response: 'results' must be a list")
    return results


def extract_pulse_data(pulses):
    data = []
    for pulse in pulses:
        data.append({
            "PulseID": pulse.get("id"),
            "Name": pulse.get("name"),
            "Created": pulse.get("created"),
            "Modified": pulse.get("modified"),
            "Description": pulse.get("description"),
            "ThreatLevel": pulse.get("threat_level"),
        })
    return pd.DataFrame(data)


if __name__ == "__main__":
    pulses = get_recent_pulses()
    df_pulses = extract_pulse_data(pulses)
    print(df_pulses.head())
    df_pulses.to_csv("cti_pulses.csv", index=False)
