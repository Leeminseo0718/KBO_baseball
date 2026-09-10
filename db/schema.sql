CREATE SCHEMA IF NOT EXISTS kbo;

CREATE TABLE IF NOT EXISTS kbo.team (
  team_id text PRIMARY KEY,
  name text NOT NULL,
  full_name text,
  valid_from date,
  valid_to date
);

CREATE TABLE IF NOT EXISTS kbo.player (
  player_id text PRIMARY KEY,
  official_name text NOT NULL,
  bats text,
  throws text,
  birth_date date,
  verified_at timestamptz
);

CREATE TABLE IF NOT EXISTS kbo.player_alias (
  source text NOT NULL,
  source_player_id text NOT NULL,
  alias_name text NOT NULL,
  player_id text REFERENCES kbo.player(player_id),
  match_status text NOT NULL DEFAULT 'pending' CHECK (match_status IN ('pending','verified','rejected')),
  matched_at timestamptz,
  PRIMARY KEY (source, source_player_id)
);

CREATE TABLE IF NOT EXISTS kbo.roster_membership (
  player_id text NOT NULL REFERENCES kbo.player(player_id),
  team_id text NOT NULL REFERENCES kbo.team(team_id),
  season integer NOT NULL,
  start_date date,
  end_date date,
  PRIMARY KEY (player_id, team_id, season, start_date)
);

CREATE TABLE IF NOT EXISTS kbo.game (
  game_id text PRIMARY KEY,
  season integer NOT NULL,
  game_date date NOT NULL,
  stadium text,
  away_team_id text REFERENCES kbo.team(team_id),
  home_team_id text REFERENCES kbo.team(team_id),
  away_score integer,
  home_score integer,
  status text NOT NULL,
  source_updated_at timestamptz
);

CREATE TABLE IF NOT EXISTS kbo.game_lineup (
  game_id text NOT NULL REFERENCES kbo.game(game_id),
  team_id text NOT NULL REFERENCES kbo.team(team_id),
  player_id text NOT NULL REFERENCES kbo.player(player_id),
  batting_order integer,
  position_name text,
  sequence_no integer NOT NULL DEFAULT 1,
  starter boolean NOT NULL DEFAULT true,
  PRIMARY KEY (game_id, team_id, player_id, sequence_no)
);

CREATE TABLE IF NOT EXISTS kbo.plate_appearance (
  game_id text NOT NULL REFERENCES kbo.game(game_id),
  sequence_no integer NOT NULL,
  inning integer NOT NULL,
  half text NOT NULL CHECK (half IN ('top','bottom')),
  batter_id text REFERENCES kbo.player(player_id),
  pitcher_id text REFERENCES kbo.player(player_id),
  outs_before smallint,
  balls_before smallint,
  strikes_before smallint,
  result_text text,
  runs_scored smallint NOT NULL DEFAULT 0,
  raw_event_type integer,
  PRIMARY KEY (game_id, sequence_no)
);

CREATE TABLE IF NOT EXISTS kbo.pitch_event (
  game_id text NOT NULL REFERENCES kbo.game(game_id),
  sequence_no integer NOT NULL,
  inning integer NOT NULL,
  half text NOT NULL CHECK (half IN ('top','bottom')),
  batter_id text REFERENCES kbo.player(player_id),
  pitcher_id text REFERENCES kbo.player(player_id),
  balls smallint,
  strikes smallint,
  outs smallint,
  event_text text NOT NULL,
  raw_event_type integer,
  PRIMARY KEY (game_id, sequence_no)
);

CREATE TABLE IF NOT EXISTS kbo.game_batting_stat (
  game_id text NOT NULL REFERENCES kbo.game(game_id),
  team_id text NOT NULL REFERENCES kbo.team(team_id),
  player_id text NOT NULL REFERENCES kbo.player(player_id),
  batting_order integer,
  plate_appearances integer,
  at_bats integer,
  hits integer,
  home_runs integer,
  walks integer,
  strikeouts integer,
  runs integer,
  rbi integer,
  stolen_bases integer,
  PRIMARY KEY (game_id, team_id, player_id)
);

CREATE TABLE IF NOT EXISTS kbo.game_pitching_stat (
  game_id text NOT NULL REFERENCES kbo.game(game_id),
  team_id text NOT NULL REFERENCES kbo.team(team_id),
  player_id text NOT NULL REFERENCES kbo.player(player_id),
  innings_outs integer,
  batters_faced integer,
  hits integer,
  home_runs integer,
  walks integer,
  strikeouts integer,
  runs integer,
  earned_runs integer,
  pitches integer,
  decision text,
  PRIMARY KEY (game_id, team_id, player_id)
);

CREATE TABLE IF NOT EXISTS kbo.source_snapshot (
  snapshot_id bigserial PRIMARY KEY,
  source text NOT NULL,
  entity_type text NOT NULL,
  source_key text NOT NULL,
  fetched_at timestamptz NOT NULL,
  source_url text NOT NULL,
  sha256 text NOT NULL,
  payload jsonb NOT NULL,
  UNIQUE (source, entity_type, source_key, sha256)
);

CREATE TABLE IF NOT EXISTS kbo.reconciliation_result (
  reconciliation_id bigserial PRIMARY KEY,
  game_id text REFERENCES kbo.game(game_id),
  check_name text NOT NULL,
  source_a_value text,
  source_b_value text,
  matched boolean NOT NULL,
  checked_at timestamptz NOT NULL DEFAULT now(),
  detail jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE OR REPLACE VIEW kbo.v_player_game_batting AS
SELECT g.game_date, g.season, t.name AS team_name, p.official_name AS player_name,
       s.plate_appearances, s.at_bats, s.hits, s.home_runs, s.walks,
       s.strikeouts, s.runs, s.rbi, s.stolen_bases
FROM kbo.game_batting_stat s
JOIN kbo.game g USING (game_id)
JOIN kbo.team t USING (team_id)
JOIN kbo.player p USING (player_id);

CREATE OR REPLACE VIEW kbo.v_player_game_pitching AS
SELECT g.game_date, g.season, t.name AS team_name, p.official_name AS player_name,
       s.innings_outs, s.batters_faced, s.hits, s.home_runs, s.walks,
       s.strikeouts, s.runs, s.earned_runs, s.pitches, s.decision
FROM kbo.game_pitching_stat s
JOIN kbo.game g USING (game_id)
JOIN kbo.team t USING (team_id)
JOIN kbo.player p USING (player_id);

REVOKE ALL ON SCHEMA kbo FROM PUBLIC;
