from database.connection import get_connection
from datetime import datetime

def upsert_match(match_data):
    """
    match_data should be a dict with:
    api_id, home_team, away_team, match_date, status, stage, home_score, away_score, etc.
    """
    conn = get_connection()
    cursor = conn.cursor()
    is_pg = 'psycopg' in str(type(conn))

    # We will use upsert via ON CONFLICT for PG and ON CONFLICT for SQLite (since we made api_id UNIQUE)
    sql_pg = """
        INSERT INTO matches (
            api_id, home_team, away_team, match_date, status, stage,
            home_score, away_score, winner, match_ending
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) ON CONFLICT (api_id) DO UPDATE SET
            home_team = EXCLUDED.home_team,
            away_team = EXCLUDED.away_team,
            match_date = EXCLUDED.match_date,
            status = EXCLUDED.status,
            stage = EXCLUDED.stage,
            home_score = EXCLUDED.home_score,
            away_score = EXCLUDED.away_score,
            winner = EXCLUDED.winner,
            match_ending = EXCLUDED.match_ending,
            updated_at = CURRENT_TIMESTAMP
    """

    sql_lite = """
        INSERT INTO matches (
            api_id, home_team, away_team, match_date, status, stage,
            home_score, away_score, winner, match_ending
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        ) ON CONFLICT (api_id) DO UPDATE SET
            home_team = excluded.home_team,
            away_team = excluded.away_team,
            match_date = excluded.match_date,
            status = excluded.status,
            stage = excluded.stage,
            home_score = excluded.home_score,
            away_score = excluded.away_score,
            winner = excluded.winner,
            match_ending = excluded.match_ending,
            updated_at = CURRENT_TIMESTAMP
    """

    params = (
        match_data['api_id'], match_data['home_team'], match_data['away_team'],
        match_data['match_date'], match_data['status'], match_data['stage'],
        match_data.get('home_score'), match_data.get('away_score'),
        match_data.get('winner'), match_data.get('match_ending')
    )

    try:
        if is_pg:
            cursor.execute(sql_pg, params)
        else:
            cursor.execute(sql_lite, params)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_all_matches():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM matches ORDER BY match_date ASC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        cursor.close()
        conn.close()

def log_sync_history(matches_updated, response_time_ms, api_used, status):
    conn = get_connection()
    cursor = conn.cursor()
    is_pg = 'psycopg' in str(type(conn))
    try:
        if is_pg:
            cursor.execute(
                "INSERT INTO sync_history (matches_updated, response_time_ms, api_used, status) VALUES (%s, %s, %s, %s)",
                (matches_updated, response_time_ms, api_used, status)
            )
        else:
            cursor.execute(
                "INSERT INTO sync_history (matches_updated, response_time_ms, api_used, status) VALUES (?, ?, ?, ?)",
                (matches_updated, response_time_ms, api_used, status)
            )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_last_sync():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM sync_history ORDER BY sync_date DESC LIMIT 1")
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        cursor.close()
        conn.close()
