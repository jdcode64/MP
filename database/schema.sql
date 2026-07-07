-- database/schema.sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'participante', -- 'admin' o 'participante'
    status VARCHAR(20) DEFAULT 'pendiente', -- 'pendiente', 'aprobado', 'inactivo'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    api_id VARCHAR(100) UNIQUE NOT NULL,
    home_team VARCHAR(100) NOT NULL,
    away_team VARCHAR(100) NOT NULL,
    match_date TIMESTAMP NOT NULL, -- Stored in UTC or local depending on parsing, will manage with pytz
    status VARCHAR(50) NOT NULL, -- 'PENDING', 'FINISHED', etc.
    stage VARCHAR(50) NOT NULL, -- 'Cuartos', 'Semifinales', etc.
    home_score INTEGER,
    away_score INTEGER,
    winner VARCHAR(50), -- 'HOME_TEAM', 'AWAY_TEAM', 'DRAW'
    first_to_score VARCHAR(50), -- 'HOME_TEAM', 'AWAY_TEAM', 'NONE'
    has_penalty BOOLEAN,
    has_red_card BOOLEAN,
    more_corners VARCHAR(50), -- 'HOME_TEAM', 'AWAY_TEAM', 'DRAW'
    team_qualified VARCHAR(100),
    match_ending VARCHAR(50), -- 'REGULAR', 'EXTRA_TIME', 'PENALTIES'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    match_id INTEGER NOT NULL REFERENCES matches(id),
    home_score INTEGER NOT NULL,
    away_score INTEGER NOT NULL,

    -- 10 Combined questions
    winner VARCHAR(50) NOT NULL, -- 'HOME_TEAM', 'AWAY_TEAM', 'DRAW'
    both_score BOOLEAN NOT NULL,
    over_2_5_goals BOOLEAN NOT NULL,
    first_to_score VARCHAR(50) NOT NULL, -- 'HOME_TEAM', 'AWAY_TEAM', 'NONE'
    has_penalty BOOLEAN NOT NULL,
    has_red_card BOOLEAN NOT NULL,
    more_corners VARCHAR(50) NOT NULL, -- 'HOME_TEAM', 'AWAY_TEAM', 'DRAW'
    team_qualified VARCHAR(100) NOT NULL,
    match_ending VARCHAR(50) NOT NULL, -- 'REGULAR', 'EXTRA_TIME', 'PENALTIES'
    total_goals_range VARCHAR(50) NOT NULL, -- '0-1', '2-3', '4_PLUS'

    -- Points calculated
    points_exact_score INTEGER DEFAULT 0,
    points_winner INTEGER DEFAULT 0,
    points_combined INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, match_id)
);

CREATE TABLE IF NOT EXISTS sync_history (
    id SERIAL PRIMARY KEY,
    sync_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    matches_updated INTEGER DEFAULT 0,
    response_time_ms INTEGER DEFAULT 0,
    api_used VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL -- 'SUCCESS', 'FAILED'
);

CREATE TABLE IF NOT EXISTS configurations (
    id SERIAL PRIMARY KEY,
    key_name VARCHAR(50) UNIQUE NOT NULL,
    key_value INTEGER NOT NULL
);

-- Insert default scoring configuration if not exists
INSERT INTO configurations (key_name, key_value) VALUES ('points_exact_score', 5) ON CONFLICT(key_name) DO NOTHING;
INSERT INTO configurations (key_name, key_value) VALUES ('points_winner', 2) ON CONFLICT(key_name) DO NOTHING;
INSERT INTO configurations (key_name, key_value) VALUES ('points_combined', 1) ON CONFLICT(key_name) DO NOTHING;
