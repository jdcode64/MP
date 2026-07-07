from database.connection import get_connection

def save_prediction(prediction_data):
    conn = get_connection()
    cursor = conn.cursor()
    is_pg = 'psycopg' in str(type(conn))

    sql_pg = """
        INSERT INTO predictions (
            user_id, match_id, home_score, away_score, winner, both_score, over_2_5_goals,
            first_to_score, has_penalty, has_red_card, more_corners, team_qualified, match_ending, total_goals_range
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) ON CONFLICT (user_id, match_id) DO UPDATE SET
            home_score = EXCLUDED.home_score,
            away_score = EXCLUDED.away_score,
            winner = EXCLUDED.winner,
            both_score = EXCLUDED.both_score,
            over_2_5_goals = EXCLUDED.over_2_5_goals,
            first_to_score = EXCLUDED.first_to_score,
            has_penalty = EXCLUDED.has_penalty,
            has_red_card = EXCLUDED.has_red_card,
            more_corners = EXCLUDED.more_corners,
            team_qualified = EXCLUDED.team_qualified,
            match_ending = EXCLUDED.match_ending,
            total_goals_range = EXCLUDED.total_goals_range,
            updated_at = CURRENT_TIMESTAMP
    """

    sql_lite = """
        INSERT INTO predictions (
            user_id, match_id, home_score, away_score, winner, both_score, over_2_5_goals,
            first_to_score, has_penalty, has_red_card, more_corners, team_qualified, match_ending, total_goals_range
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        ) ON CONFLICT (user_id, match_id) DO UPDATE SET
            home_score = excluded.home_score,
            away_score = excluded.away_score,
            winner = excluded.winner,
            both_score = excluded.both_score,
            over_2_5_goals = excluded.over_2_5_goals,
            first_to_score = excluded.first_to_score,
            has_penalty = excluded.has_penalty,
            has_red_card = excluded.has_red_card,
            more_corners = excluded.more_corners,
            team_qualified = excluded.team_qualified,
            match_ending = excluded.match_ending,
            total_goals_range = excluded.total_goals_range,
            updated_at = CURRENT_TIMESTAMP
    """

    params = (
        prediction_data['user_id'], prediction_data['match_id'], prediction_data['home_score'],
        prediction_data['away_score'], prediction_data['winner'], prediction_data['both_score'],
        prediction_data['over_2_5_goals'], prediction_data['first_to_score'], prediction_data['has_penalty'],
        prediction_data['has_red_card'], prediction_data['more_corners'], prediction_data['team_qualified'],
        prediction_data['match_ending'], prediction_data['total_goals_range']
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

def get_user_predictions(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    is_pg = 'psycopg' in str(type(conn))
    try:
        if is_pg:
            cursor.execute("SELECT * FROM predictions WHERE user_id = %s", (user_id,))
        else:
            cursor.execute("SELECT * FROM predictions WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        cursor.close()
        conn.close()

def get_all_predictions():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM predictions")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        cursor.close()
        conn.close()

def update_prediction_points(prediction_id, points_exact, points_winner, points_combined, total):
    conn = get_connection()
    cursor = conn.cursor()
    is_pg = 'psycopg' in str(type(conn))
    try:
        if is_pg:
            cursor.execute("""
                UPDATE predictions
                SET points_exact_score = %s, points_winner = %s, points_combined = %s, total_points = %s
                WHERE id = %s
            """, (points_exact, points_winner, points_combined, total, prediction_id))
        else:
            cursor.execute("""
                UPDATE predictions
                SET points_exact_score = ?, points_winner = ?, points_combined = ?, total_points = ?
                WHERE id = ?
            """, (points_exact, points_winner, points_combined, total, prediction_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
