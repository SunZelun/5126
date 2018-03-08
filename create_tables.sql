CREATE TABLE seasons (
    season_id INT (4)     PRIMARY KEY
                          UNIQUE
                          NOT NULL,
    name      STRING (10),
    type      STRING (8)  NOT NULL
                          DEFAULT NBA
)
WITHOUT ROWID;


CREATE TABLE colleges (
    college_id INTEGER      PRIMARY KEY
                            UNIQUE
                            NOT NULL,
    name       STRING (100) NOT NULL
)
WITHOUT ROWID;

CREATE TABLE teams (
    team_id              INTEGER      PRIMARY KEY
                                      NOT NULL
                                      UNIQUE,
    [from]               INTEGER (4),
    [to]                 INTEGER,
    total_years          INTEGER (4),
    games_played         INTEGER (10),
    wins                 INTEGER (10),
    losses               INTEGER (10),
    playoffs_appearences INTEGER (10) 
)
WITHOUT ROWID;

CREATE TABLE players (
    player_id INTEGER      PRIMARY KEY
                           UNIQUE
                           NOT NULL,
    age       INTEGER (3),
    name      STRING (100) NOT NULL,
    weight    INTEGER (4),
    height    INTEGER (4),
    dob       DATE
)
WITHOUT ROWID;

CREATE TABLE college_player_stats (
    college_id       INTEGER      REFERENCES colleges (college_id) ON DELETE NO ACTION
                                                                   ON UPDATE NO ACTION
                                  NOT NULL,
    player_id        INTEGER      REFERENCES players (player_id) ON DELETE NO ACTION
                                                                 ON UPDATE NO ACTION
                                  NOT NULL,
    season_id        INTEGER      REFERENCES seasons (season_id) ON DELETE NO ACTION
                                                                 ON UPDATE NO ACTION
                                  NOT NULL,
    age              INTEGER (4),
    game_played      INTEGER (4)  DEFAULT (0),
    minutes_played   INTEGER (10) DEFAULT (0),
    points           INTEGER (10) DEFAULT (0),
    field_goal       INTEGER (10) DEFAULT (0),
    field_goal_total INTEGER (10) DEFAULT (0),
    assist           INTEGER (10) DEFAULT (0),
    total_rb         INTEGER (10) DEFAULT (0),
    steal            INTEGER (10) DEFAULT (0),
    block            INTEGER (10) DEFAULT (0),
    turnover         INTEGER (10) DEFAULT (0),
    PRIMARY KEY ( college_id, player_id, season_id)
)
WITHOUT ROWID;

CREATE TABLE team_player_salary (
    player_id INTEGER      REFERENCES players (player_id) ON DELETE NO ACTION
                                                          ON UPDATE NO ACTION,
    team_id   INTEGER      REFERENCES teams (team_id) ON DELETE NO ACTION
                                                      ON UPDATE NO ACTION,
    season_id INTEGER      REFERENCES seasons (season_id) ON DELETE NO ACTION
                                                          ON UPDATE NO ACTION,
    salary    DECIMAL (12) DEFAULT (0),
    PRIMARY KEY ( player_id, team_id, season_id)
)
WITHOUT ROWID;

CREATE TABLE nba_player_stats (
    player_id INTEGER REFERENCES players (player_id) ON DELETE NO ACTION
                                                     ON UPDATE NO ACTION,
    season_id INTEGER REFERENCES seasons (season_id) ON DELETE NO ACTION
                                                     ON UPDATE NO ACTION,
    team_id   INTEGER REFERENCES teams (team_id) ON DELETE NO ACTION
                                                 ON UPDATE NO ACTION,
    age    INTEGER DEFAULT (0),
    position    INTEGER DEFAULT (0),
    minutes_played    INTEGER DEFAULT (0),
    game_played    INTEGER DEFAULT (0),
    points    INTEGER DEFAULT (0),
    assist    INTEGER DEFAULT (0),
    field_goal    INTEGER DEFAULT (0),
    field_goal_total    INTEGER DEFAULT (0),
    effective_field_goal    DECIMAL DEFAULT (0),
    off_rb    INTEGER DEFAULT (0),
    def_rb    INTEGER DEFAULT (0),
    steal    INTEGER DEFAULT (0),
    block    INTEGER DEFAULT (0),
    stats_type    INTEGER DEFAULT (0),
    turnover    INTEGER DEFAULT (0),
    PRIMARY KEY ( player_id, season_id, team_id )
)
WITHOUT ROWID;
