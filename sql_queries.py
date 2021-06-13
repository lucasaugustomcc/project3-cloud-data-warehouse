import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
DWH_ROLE_ARN = config.get("IAM_ROLE","ARN")
LOG_DATA = config.get("S3","LOG_DATA")
LOG_JSONPATH = config.get("S3","LOG_JSONPATH")
SONG_DATA = config.get("S3","SONG_DATA")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE staging_events (
        artist varchar,
        auth varchar,
        first_name varchar,
        gender char(1),
        item_in_session int,
        last_name varchar,
        length numeric,
        level varchar,
        location varchar,
        method varchar,
        page varchar,
        registration numeric,
        session_id int,
        song varchar,
        status int,
        ts bigint,
        user_agent varchar,
        user_id int
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE staging_songs (
        num_songs int,
        artist_id varchar,
        artist_latitude varchar,
        artist_longitude varchar,
        artist_location varchar,
        artist_name varchar,
        song_id varchar,
        title varchar,
        duration numeric,
        year int
    )
""")

songplay_table_create = ("""
    CREATE TABLE songplays (
        songplay_id INT IDENTITY(0,1) PRIMARY KEY,
        start_time TIMESTAMP WITHOUT TIME ZONE NOT NULL
            REFERENCES time(start_time),
        user_id int NOT NULL
            REFERENCES users(user_id),
        level varchar,
        song_id varchar
            REFERENCES songs(song_id),
        artist_id varchar
             REFERENCES artists(artist_id),
        session_id int,
        location varchar,
        user_agent varchar)
""")

user_table_create = ("""
    CREATE TABLE users (
        user_id int PRIMARY KEY,
        first_name varchar,
        last_name varchar,
        gender char(1),
        level varchar
    )
""")

song_table_create = ("""
    CREATE TABLE songs (
        song_id varchar PRIMARY KEY,
        title varchar,
        artist_id varchar REFERENCES artists(artist_id),
        year int,
        duration numeric
    )
""")

artist_table_create = ("""
    CREATE TABLE artists (
        artist_id varchar PRIMARY KEY,
        name varchar,
        location varchar,
        latitude numeric,
        longitude numeric
    )
""")

time_table_create = ("""
    CREATE TABLE time (
        start_time TIMESTAMP WITHOUT TIME ZONE PRIMARY KEY,
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday int
    )
""")

# STAGING TABLES

staging_events_copy = ("""
    copy {} from '{}' 
    credentials 'aws_iam_role={}'
    region 'us-west-2'
    json 's3://udacity-dend/log_json_path.json';
""").format('staging_events', LOG_DATA, DWH_ROLE_ARN)

staging_songs_copy = ("""
    copy {} from '{}' 
    credentials 'aws_iam_role={}'
    format as json 'auto' region 'us-west-2';
""").format('staging_songs', SONG_DATA, DWH_ROLE_ARN)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (
        start_time,
        user_id,
        level,
        song_id,
        artist_id,
        session_id,
        location,
        user_agent
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
    SELECT user_id, first
    INSERT into users (user_id, first_name, last_name, gender, level)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT(user_id) DO UPDATE SET level = excluded.level
""")

song_table_insert = ("""
    INSERT into songs (song_id, title, artist_id, year, duration)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT(song_id) DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT(artist_id) DO NOTHING;
""")


time_table_insert = ("""
    INSERT into time (start_time, hour, day, month, week, weekday, year)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT(start_time) DO NOTHING;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, artist_table_create, time_table_create, user_table_create, song_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_songs_copy, staging_events_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
