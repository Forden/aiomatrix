create table internal_data
(
    account_id TEXT,
    key        TEXT,
    data       TEXT,
    UNIQUE (account_id, key) ON CONFLICT ABORT,
    PRIMARY KEY (account_id, key)
);


create table seen_events
(
    account_id TEXT,
    event_ID   TEXT,
    UNIQUE (account_id, event_id) ON CONFLICT IGNORE,
    PRIMARY KEY (account_id, event_id)
);


create table events
(
    event_id   TEXT,
    ts         INTEGER,
    room_id    TEXT,
    sender     TEXT,
    event_type TEXT,
    data       TEXT,
    UNIQUE (event_id) ON CONFLICT IGNORE,
    PRIMARY KEY (event_id)
);


create table presence
(
    account_id  TEXT,
    user_id     TEXT,
    presence    TEXT,
    last_active INTEGER,
    status_msg  TEXT,
    last_update INTEGER,
    UNIQUE (account_id, user_id) ON CONFLICT IGNORE,
    PRIMARY KEY (account_id, user_id)
);
