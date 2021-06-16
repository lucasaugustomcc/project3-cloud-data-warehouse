# Project: Cloud Data Warehouse
## Summary of the Project
Sparkify is a startup which wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. 

In this document I will provide discussion on the process and decisions for the ETL pipeline.

## Files in the Repository
The project includes three files:
- *create_table.py*: creates the fact and dimension tables for the star schema in Redshift.
- *etl.py*: loads data from S3 into staging tables on Redshift and then processes that data into analytics tables on Redshift.
- *sql_queries.py*: defines the SQL statements, which will be imported into the two other files above.

## Configuration File
```INI
[CLUSTER]
HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=

[IAM_ROLE]
ARN=

[S3]
LOG_DATA=s3://udacity-dend/log_data
LOG_JSONPATH=s3://udacity-dend/log_json_path.json
SONG_DATA=s3://udacity-dend/song_data
```

## How to run the Python scripts
1. Run *create_tables.py* to create the database and tables.
2. Run *etl.py* to load the data into the project's tables.

# Database schema

## Staging Tables

### Events
| column          | type      |
| ----------------|:---------:| 
| artist          | varchar   | 
| auth            | varchar   | 
| first_name      | varchar   | 
| gender          | char(1)   | 
| item_session_id | int       |
| last_name       | varchar   | 
| length          | numeric   |
| level           | varchar   |
| location        | varchar   |
| method          | varchar   |
| page            | varchar   |
| registration    | numeric   |
| session_id      | int       |
| song            | varchar   | 
| status          | int       |
| ts              | bigint    |
| user_agent      | varchar   |
| user_id         | int       |

### Songs
| column           | type    |
| -----------------|:-------:|
| num_songs        | int     |
| artist_id        | varchar |
| artist_latitude  | numeric |
| artist_longitude | numeric |
| artist_location  | varchar |
| artist_name      | varchar |
| song_id          | varchar |
| title            | varchar |
| duration         | float   |
| year             | int     |

## Fact Tables
### songplays 
Records in log data associated with song plays

| column        | type          |
| ------------- |:-------------:| 
| songplay_id   | serial (PK)   | 
| start_time    | TIMESTAMP (FK)|
| user_id       | int (FK)      |
| level         | varchar       |
| song_id       | varchar (FK)  | 
| artist_id     | varchar (FK)  |
| session_id    | int           |
| location      | varchar       |
| user_agent    | varchar       |

## Dimension Tables
### users
users in the app

| column        | type          |
| ------------- |:-------------:| 
| user_id       | int (PK)      |
| first_name    | varchar       |
| last_name     | varchar       |
| gender        | char(1)       |
| level         | varchar       |

### songs
songs in music database

| column        | type          |
| ------------- |:-------------:|
| song_id       | varchar (PK)  |
| title         | varchar       |
| artist_id     | varchar (FK)  |
| year          | int           |
| duration      | numeric       |

### artists
artists in music database
| column        | type          |
| ------------- |:-------------:|
| artist_id     | varchar (PK)  |
| name          | varchar       |
| location      | varchar       |
| latitude      | numeric       |
| longitude     | numeric       |

### time
timestamps of records in songplays broken down into specific units
| column        | type          |
| ------------- |:-------------:|
| start_time    | TIMESTAMP (PK)|
| hour          | int           |
| day           | int           |
| week          | int           |
| month         | int           |
| year          | int           |
| weekday       | int           |
