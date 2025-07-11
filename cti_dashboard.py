import requests
import pandas as pd

API_KEY = '563030eefecea571ba5ce9805bbc919a1536e3377fa5a31e82b76a09a601043e'
BASE_URL = 'https://otx.alienvault.com/api/v1'

HEADERS = {
    'X-OTX-API-KEY': API_KEY
}

def get_recent_pulses(limit=50):
    url = f"{BASE_URL}/pulses/subscribed"
    params = {'limit': limit}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f"Error fetching pulses: {response.status_code}")
        return []

def extract_pulse_data(pulses):
    # Extract key details into a list of dicts
    data = []
    for pulse in pulses:
        pulse_id = pulse.get('id')
        name = pulse.get('name')
        created = pulse.get('created')
        modified = pulse.get('modified')
        description = pulse.get('description')
        threat_level = pulse.get('threat_level')
        data.append({
            'PulseID': pulse_id,
            'Name': name,
            'Created': created,
            'Modified': modified,
            'Description': description,
            'ThreatLevel': threat_level
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    pulses = get_recent_pulses()
    df_pulses = extract_pulse_data(pulses)
    print(df_pulses.head())
    # Save to CSV for Power BI ingestion
    df_pulses.to_csv('cti_pulses.csv', index=False)
