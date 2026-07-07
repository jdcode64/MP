import requests
import time
from datetime import datetime
from repositories.match_repo import upsert_match, log_sync_history
from utils.time_utils import to_bogota_time

def fetch_football_data():
    # Placeholder for actual API call, just a structural implementation
    # Normally we would need an API Key for football-data.org
    # This is mock implementation since API keys are not provided.
    return []

def fetch_the_sports_db():
    # TheSportsDB public API doesn't require key for some endpoints but we need a valid endpoint
    # E.g. https://www.thesportsdb.com/api/v1/json/3/eventsseason.php?id=4362&s=2026
    # For now, return mock or handle exceptions
    return []

def sync_matches_to_db():
    start_time = time.time()
    api_used = "football-data.org"
    matches = []

    try:
        # We try to fetch from primary
        matches = fetch_football_data()
        if not matches:
            raise Exception("No data from primary")
    except Exception as e:
        # Fallback to secondary
        api_used = "TheSportsDB (Fallback)"
        try:
            matches = fetch_the_sports_db()
        except:
            pass

    # If we had real data we would map it here
    # Since it's a demonstration for 2026 World Cup which might not have data yet in APIs:
    # We will simulate a couple of matches to have something in DB if empty.
    # In real world, we parse the JSON and map to our match_data format.

    if not matches:
        # Mocking some data for demonstration
        api_used = "Mock API (No data found)"
        mock_matches = [
            {
                'api_id': 'match_1',
                'home_team': 'Colombia',
                'away_team': 'Brasil',
                'match_date': '2026-06-15T15:00:00Z', # UTC
                'status': 'PENDING',
                'stage': 'Fase de grupos',
                'home_score': None,
                'away_score': None,
                'winner': None,
                'match_ending': 'REGULAR'
            },
            {
                'api_id': 'match_2',
                'home_team': 'Argentina',
                'away_team': 'Francia',
                'match_date': '2026-06-16T18:00:00Z', # UTC
                'status': 'PENDING',
                'stage': 'Fase de grupos',
                'home_score': None,
                'away_score': None,
                'winner': None,
                'match_ending': 'REGULAR'
            }
        ]
        matches = mock_matches

    matches_updated = 0
    for m in matches:
        # Convert date to our naive UTC or parse it
        try:
            dt = datetime.strptime(m['match_date'], "%Y-%m-%dT%H:%M:%SZ")
        except:
            dt = datetime.now() # Fallback

        match_data = {
            'api_id': m['api_id'],
            'home_team': m['home_team'],
            'away_team': m['away_team'],
            'match_date': dt,
            'status': m['status'],
            'stage': m['stage'],
            'home_score': m['home_score'],
            'away_score': m['away_score'],
            'winner': m['winner'],
            'match_ending': m['match_ending']
        }
        upsert_match(match_data)
        matches_updated += 1

    end_time = time.time()
    response_time_ms = int((end_time - start_time) * 1000)

    log_sync_history(matches_updated, response_time_ms, api_used, 'SUCCESS')
    return matches_updated, response_time_ms, api_used
