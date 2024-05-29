import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

API_KEY = '7765fab0d40bbcf156b6c01896c8b364'
SPORTS = 'upcoming'
REGIONS = 'us,us2,uk,au,eu'
MARKETS = 'alternate_spreads'
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'

counter = 0

def get_in_season_sports() -> list:
    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports', 
        params={
            'api_key': API_KEY,
            'outrights': 'false'
        }
    )
    
    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
    else:
        sports = []
        for response in sports_response.json():
            sports.append(response["key"])
        return sports


def get_event_ids(sport: str) -> list:
    http_request = f'https://api.the-odds-api.com/v4/sports/{sport}/events'
    dt_from = datetime.now().replace(microsecond=0).isoformat()
    time_from = f'{dt_from}Z'
    event_response = requests.get(
        http_request,
        params={
            'api_key': API_KEY,
            'dateFormat': DATE_FORMAT,
            'commenceTimeFrom': time_from,
        }
    )

    if event_response.status_code != 200:
        print(f'Failed to get sports: status_code {event_response.status_code}, response body {event_response.text}')
    else:
        event_ids = []
        for event in event_response.json():
            event_dict = {'id': event['id'], 'team1': event['home_team'], 'team2': event['away_team'], 'dt': event['commence_time']}
            event_ids.append(event_dict)
        return event_ids


def get_event_odds(sport:str, eventId: str) -> list:
    http_request = f'https://api.the-odds-api.com/v4/sports/{sport}/events/{eventId}/odds?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}&dateFormat={DATE_FORMAT}&oddsFormat={ODDS_FORMAT}'
    odds_response = requests.get(http_request)
    if odds_response.status_code != 200:
        print(f'Failed to get sports: status_code {odds_response.status_code}, response body {odds_response.text}')
    else:
        odds = []
        for bookmaker in odds_response.json()['bookmakers']:
            bookmaker_key = bookmaker['key']
            outcomes = bookmaker['markets'][0]['outcomes']
            for outcome in outcomes:
                price = outcome['price']
                point = outcome['point']
                team = outcome['name']     
                odds.append({'bookmaker': bookmaker_key, 'price': price, 'line': point, 'team': team})
        return odds