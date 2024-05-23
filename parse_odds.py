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


def get_event_odds(sport:str, eventId: str) -> dict:
    http_request = f'https://api.the-odds-api.com/v4/sports/{sport}/events/{eventId}/odds?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}&dateFormat={DATE_FORMAT}&oddsFormat={ODDS_FORMAT}'
    odds_response = requests.get(http_request)

    if odds_response.status_code != 200:
        print(f'Failed to get sports: status_code {odds_response.status_code}, response body {odds_response.text}')
    else:
        prices = []
        points = []
        for bookmaker in odds_response.json()['bookmakers']:
            outcomes = bookmaker['markets'][0]['outcomes']
            for outcome in outcomes:
                price = outcome['price']
                point = outcome['point']
                prices.append(price)
                points.append(point)
                # print(f'Price:{price}')
                # print(f'Point:{point}')
                # print()
    return {'prices': prices, 'points': points}

if __name__ == "__main__":
    # for sport in get_in_season_sports():
    #     for event in get_event_ids(sport):
    #         get_event_odds(sport, event)
    get_event_odds('americanfootball_ncaaf', '329ee4daba3514dce8018d5768e5043f')

def compile_event_ids() -> list:
    ids = []
    for sport in get_in_season_sports():
        for id in get_event_ids(sport):
            ids.append(id)

    return ids