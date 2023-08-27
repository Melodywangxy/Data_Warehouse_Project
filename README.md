# Data_Warehouse_Project
The purpose of this project is to create a redshift database of song and user activity for Sparkify's new music streaming app. This will allow them to analyze their data which currently resides in a directory of JSON logs and JSON metadata.
# Business Process / Data Requirements
  1. Analytics team wants to understand what songs their users are listening to by analyzing a set of dimensional tables.
  2. Analytics team wants a Data warehouse on the cloud with tables designed to optimize queries and gain insights on song plays.
# Engineering Task
### Create and launch a Redshift cluster on AWS
  Create a Redshift cluster and IAM role to grant access to S3
### Create a star schema and ETL pipeline to prepare the data for analytics team.  
  A. Explore & load raw data (JSON) in S3 to Redshift staging tables  
  B. Define fact & dimension tables for a star schema for this particular analytic purpose  
  C. Write an ETL pipeline to load data from staging tables to analytics tables on Redshift  
### Connect to the Redshift cluster and run some test queries
# Schema for Song Play Analysis
##  Fact Table  
songplays - records in event data associated with song plays i.e. records with page NextSong  
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent  
##  Dimension Tables  
**-users - users in the app**<br>
user_id, first_name, last_name, gender, level  
**-songs - songs in music database**<br>
song_id, title, artist_id, year, duration  
**-artists - artists in music database**<br>
artist_id, name, location, lattitude, longitude  
**-time - timestamps of records in songplays broken down into specific units**<br>
start_time, hour, day, week, month, year, weekday
# Files
### create_tables.py
The script is to connect redshift,  drops and creates tables: staging_events, staging_songs, songplays, users ,artists,songs, time tables.

### etl.py
This script copies all log and song JSON files from S3 to redshift staging tables, and then inserts the data into analytic star schema tables in the redshift datawarehouse.

### sql_queries.py
Contains SQL queries used by create_tables.py and etl.py to create, drop, and insert data.

### dwh.cfg
Contains configuration data needed to connect to S3 and redshift database. Syntax as follows:

<code>[CLUSTER]
HOST=''
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_PORT=

[IAM_ROLE]
ARN=''

[S3]
LOG_DATA=''
LOG_JSONPATH=''
SONG_DATA=''</code>

### test_notebook.ipynb
This is the test codes in Jupiter notebook and for check the results.


# Original Data Sources
Note that the actual data (in JSON) used in this project is a subset of original dataset preprocessed by the course. The provided data resides in AWS S3 (publically available).

1. Song data from Million Song Dataset
2. User activity data from Event Simulator based on Million Song Dataset

# Project Steps
Below are steps to complete each component of this project.

## Create Table Schemas
1. Design schemas for fact and dimension tables
2. Write SQL CREATE statement for each of these tables in sql_queries.py
3. Complete the logic in create_tables.py to connect to the database and create these tables
4. Write SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. This way, can run create_tables.py. whenever resetdatabase and test ETL pipeline.
5. Launch a redshift cluster and create an IAM role that has read access to S3.
6. Add redshift database and IAM role info to dwh.cfg.
7. Test by running create_tables.py and checking the table schemas in your redshift database. 
## Build ETL Pipeline
1. Implement the logic in etl.py to load data from S3 to staging tables on Redshift.
2. Implement the logic in etl.py to load data from staging tables to analytics tables on Redshift.
3. Test by running etl.py after running create_tables.py and running the analytic queries on your Redshift database to compare your results with the expected results.
4. Delete your redshift cluster when finished.

# Queries examples

 > **Please be noted that to save the time of copy staging_songs file, I use 's3://udacity-dend/song-data/A/A' as loading file, which results to the less records in songplays table.**
### Top 5 Most Played Songs with artist name


 <code>%%sql
​
SELECT  s.title, a.name, COUNT(*) 
FROM songplays p
JOIN songs  s
ON p.song_id = s.song_id 
JOIN artists a
ON a.artist_id = p.artist_id
GROUP BY 1,2
ORDER BY 3 DESC 
LIMIT 5;</code>
 
![Tux, the Linux mascot](https://github.com/Melodywangxy/Data_Warehouse_Project/blob/main/Image/1topsongs.png)
### Paid user vs free user

<code>%%sql
​
SELECT  level, COUNT(*)
FROM songplays 
GROUP BY 1;</code><br>

![Tux, the Linux mascot](https://github.com/Melodywangxy/Data_Warehouse_Project/blob/main/Image/2paidUser.png)
### Top 5 Most popular artist

<code>%%sql
​
SELECT a.name, count(*)
FROM songplays p
JOIN artists a
ON p.artist_id = a.artist_id
GROUP BY 1
ORDER BY count DESC
LIMIT 5;</code> <br>

![Tux, the Linux mascot](https://github.com/Melodywangxy/Data_Warehouse_Project/blob/main/Image/3topartists.png)

