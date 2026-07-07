from repositories.prediction_repo import get_all_predictions, update_prediction_points
from repositories.match_repo import get_all_matches
from repositories.config_repo import get_scoring_config

def calculate_prediction_points():
    """
    Recalculates points for all predictions based on current match results.
    """
    matches = {m['id']: m for m in get_all_matches()}
    predictions = get_all_predictions()
    configs = get_scoring_config()

    p_exact = int(configs.get('points_exact_score', 5))
    p_winner = int(configs.get('points_winner', 2))
    p_combined = int(configs.get('points_combined', 1))

    for p in predictions:
        match = matches.get(p['match_id'])
        if not match or match['status'] != 'FINISHED':
            continue

        pts_exact = 0
        pts_winner = 0
        pts_combined = 0

        # Check exact score
        if match['home_score'] == p['home_score'] and match['away_score'] == p['away_score']:
            pts_exact = p_exact

        # Check winner
        # Determine match winner from score if not explicitly set
        m_winner = 'DRAW'
        if match['home_score'] > match['away_score']:
            m_winner = 'HOME_TEAM'
        elif match['away_score'] > match['home_score']:
            m_winner = 'AWAY_TEAM'

        if p['winner'] == m_winner:
            pts_winner = p_winner

        # Combine questions (Mock logic, would need actual match data to verify completely)
        # For example, if we knew both scored:
        m_both_score = (match['home_score'] > 0 and match['away_score'] > 0)
        if p['both_score'] == m_both_score:
            pts_combined += p_combined

        m_over_2_5 = ((match['home_score'] + match['away_score']) > 2)
        if p['over_2_5_goals'] == m_over_2_5:
            pts_combined += p_combined

        # ... logic for other combined points ...
        # (Assuming they match for demonstration if we don't have the data from API)

        total = pts_exact + pts_winner + pts_combined

        update_prediction_points(p['id'], pts_exact, pts_winner, pts_combined, total)

def get_leaderboard_data():
    from repositories.user_repo import get_all_users
    users = {u['id']: u for u in get_all_users()}
    predictions = get_all_predictions()

    leaderboard = {}
    for p in predictions:
        uid = p['user_id']
        if uid not in leaderboard:
            leaderboard[uid] = {
                'name': f"{users[uid]['first_name']} {users[uid]['last_name']}",
                'total_points': 0,
                'exact_scores': 0,
                'winners': 0,
                'combined': 0
            }
        leaderboard[uid]['total_points'] += p['total_points']
        if p['points_exact_score'] > 0:
            leaderboard[uid]['exact_scores'] += 1
        if p['points_winner'] > 0:
            leaderboard[uid]['winners'] += 1
        leaderboard[uid]['combined'] += p['points_combined']

    # Convert to list and sort
    # Desempate: 1. Puntos, 2. Exactos, 3. Ganadores, 4. Combinadas
    result = list(leaderboard.values())
    result.sort(key=lambda x: (x['total_points'], x['exact_scores'], x['winners'], x['combined']), reverse=True)

    return result
