import requests
import datetime

API_KEY = '572ebdf0a5246419c13bf503b00cefaf'
SPORTS = 'upcoming'
REGIONS = 'us,us2'
MARKETS = 'alternate_spreads'
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'

def get_in_season_sports() -> list:
    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports', 
        params={
            'api_key': API_KEY
        }
    )
    
    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
    else:
        sports = []
        for response in sports_response.json():
            sports.append(response["key"])
        return sports


def get_event_ids(sport: str):
    http_request = f'https://api.the-odds-api.com/v4/sports/{sport}/events'
    dt = datetime.datetime.now().replace(microsecond=0).isoformat()
    time_from = f'{dt}Z'
    event_response = requests.get(
        http_request,
        params={
            'api_key': API_KEY,
            'dateFormat': DATE_FORMAT,
            'commenceTimeFrom': time_from
        }
    )

    if event_response.status_code != 200:
        print(f'Failed to get sports: status_code {event_response.status_code}, response body {event_response.text}')
    else:
        event_ids = []
        for event in event_response.json():
            event_ids.append(event['id'])
        return event_ids


if __name__ == "__main__":
    ids = []
    for sport in get_in_season_sports():
        for id in get_event_ids(sport):
            ids.append(id)

    print(ids)