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

# Original Data Sources
Note that the actual data (in JSON) used in this project is a subset of original dataset preprocessed by the course. The provided data resides in AWS S3 (publically available).

1. Song data from Million Song Dataset
2. User activity data from Event Simulator based on Million Song Dataset

# Project Steps
Below are steps you can follow to complete each component of this project.

## Create Table Schemas
1. Design schemas for your fact and dimension tables
2. Write a SQL CREATE statement for each of these tables in sql_queries.py
3. Complete the logic in create_tables.py to connect to the database and create these tables
4. Write SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. This way, you can run create_tables.py. whenever you want to reset your database and test your ETL pipeline.
5. Launch a redshift cluster and create an IAM role that has read access to S3.
6. Add redshift database and IAM role info to dwh.cfg.
7. Test by running create_tables.py and checking the table schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.
## Build ETL Pipeline
1. Implement the logic in etl.py to load data from S3 to staging tables on Redshift.
2. Implement the logic in etl.py to load data from staging tables to analytics tables on Redshift.
3. Test by running etl.py after running create_tables.py and running the analytic queries on your Redshift database to compare your results with the expected results.
4. Delete your redshift cluster when finished.

# Queries examples

### Top 5 Most Played Songs


 <code>%%sql
​
SELECT songplays.song_id, songs.title, COUNT(*) 
FROM songplays 
JOIN songs  
ON songplays.song_id = songs.song_id 
GROUP BY 1,2  
ORDER BY COUNT DESC 
LIMIT 5;</code>
 

### Top 5 Most Used Browsers

<code>%%sql
​
SELECT  user_agent, COUNT(*)
FROM songplays 
GROUP BY user_agent 
ORDER BY  COUNT DESC 
LIMIT 5;</code>
 
### Top 5 Most popular artist

<code>%%sql
​
SELECT a.name, count(*)
FROM songplays p
JOIN artists a
ON p.artist_id = a.artist_id
GROUP BY 1
ORDER BY count DESC
LIMIT 5;</code>


