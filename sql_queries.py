import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA  = config.get("S3", "LOG_DATA")
LOG_PATH  = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")
IAM_ROLE  = config.get("IAM_ROLE","ARN")
# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events(
        artist varchar,
        auth varchar,
        firstName varchar,
        gender varchar,
        ItemInSession int,
        lastName varchar,
        length float,
        level varchar,
        location varchar,
        method varchar,
        page varchar,
        registration varchar,
        sessionId int,
        song varchar,
        status int,
        ts bigint, 
        userAgent varchar, 
        userId int
);

""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs           int,
    artist_id           varchar(50),
    artist_latitude     float,
    artist_longitude    float,
    artist_location     varchar(256),
    artist_name         varchar(256),
    song_id             varchar(50),
    title               varchar(256),
    duration            float,
    year                int
);

""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays(
        songplay_id         int identity(0,1) primary key,
        start_time          timestamp NOT NULL sortkey distkey,
        user_id             int NOT NULL,
        level               varchar,
        song_id             varchar NOT NULL,
        artist_id           varchar NOT NULL,
        session_id          int,
        location            varchar,
        user_agent          varchar
);



""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
        user_id varchar(50) NOT NULL PRIMARY KEY,
        first_name varchar(256),
        last_name varchar(256),
        gender varchar(50),
        level varchar(10)
);

""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs(
        song_id varchar(50) NOT NULL PRIMARY KEY,
        title varchar NOT NULL,
        artist_id varchar(50) NOT NULL,
        year int,
        duration float
);

""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(
        artist_id varchar(50) NOT NULL PRIMARY KEY,
        name varchar(256),
        location varchar(256),
        latitude varchar,
        longitude varchar
);

""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time
    (
        start_time  timestamp NOT NULL PRIMARY KEY distkey sortkey,
        hour        int NOT NULL,
        day         int NOT NULL,
        week        int NOT NULL,
        month       int NOT NULL,
        year        int NOT NULL,
        weekday     varchar(10) NOT NULL
); 

""")

# STAGING TABLES

staging_events_copy = ("""COPY staging_events FROM {}
IAM_ROLE {}
JSON 's3://udacity-dend/log_json_path.json'
region 'us-west-2';
""").format(LOG_DATA, IAM_ROLE)

staging_songs_copy = ("""
copy staging_songs from {}
    IAM_ROLE {}
    region      'us-west-2'
    format       as JSON 'auto'
""").format(SONG_DATA, IAM_ROLE)

# FINAL TABLES

songplay_table_insert = ("""
        insert into songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT TIMESTAMP 'epoch' + (e.ts / 1000) * INTERVAL '1 second' as start_time, 
        e.userId        as user_id, 
        e.level         as level, 
        s.song_id       as song_id, 
        s.artist_id     as artist_id, 
        e.sessionId     as session_id, 
        e.location      as location, 
        e.userAgent     as user_agent
    from staging_events e
    join staging_songs  s
    on e.song = s.title and e.artist = s.artist_name and e.page = 'NextSong' and e.length = s.duration
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name,
                        gender, level)
                        SELECT DISTINCT e.userId AS user_id,
                        e.firstName AS first_name,
                        e.lastName AS last_name,
                        e.gender,
                        e.level
                        FROM staging_events e
                        where user_id is not null
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, 
                        year, duration)
                        SELECT DISTINCT song_id,
                        title,
                        artist_id,
                        year,
                        duration
                        FROM staging_songs
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, 
                        latitude, longitude)
                        SELECT DISTINCT artist_id,
                        artist_name AS name,
                        artist_location AS location,
                        artist_latitude AS latitude,
                        artist_longitude AS longitude
                        FROM staging_songs

""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, 
                        year, weekday)
                        SELECT DISTINCT(DATEADD(s, ts/1000, '19700101')) AS start_time,
                        EXTRACT(hour from start_time) AS hour,
                        EXTRACT(day from start_time) AS day,
                        EXTRACT(week from start_time) AS week,
                        EXTRACT(month from start_time) AS month,
                        EXTRACT(year from start_time) AS year,
                        EXTRACT(weekday from start_time) AS weekday
                        FROM staging_events
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
