# Data_Warehouse_Project
The purpose of this project is to create a redshift database of song and user activity for Sparkify's new music streaming app. This will allow them to analyze their data which currently resides in a directory of JSON logs and JSON metadata.
# Business Process / Data Requirements
  1. Analytics team wants to understand what songs their users are listening to by analyzing a set of dimensional tables.
  2. Analytics team wants a Data warehouse on the cloud with tables designed to optimize queries and gain insights on song plays.
# Engineering Task
1. Create and launch a Redshift cluster on AWS
  Create a Redshift cluster and IAM role to grant access to S3
2. Create a star schema and ETL pipeline to prepare the data for analytics team.  
  A. Explore & load raw data (JSON) in S3 to Redshift staging tables  
  B. Define fact & dimension tables for a star schema for this particular analytic purpose  
  C. Write an ETL pipeline to load data from staging tables to analytics tables on Redshift  
3. Connect to the Redshift cluster and run some test queries
# Schema for Song Play Analysis
1. Fact Table  
songplays - records in event data associated with song plays i.e. records with page NextSong  
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent  
2. Dimension Tables  
**-users - users in the app  **
user_id, first_name, last_name, gender, level  
**-songs - songs in music database  **
song_id, title, artist_id, year, duration  
**-artists - artists in music database  **
artist_id, name, location, lattitude, longitude  
**-time - timestamps of records in songplays broken down into specific units  **
start_time, hour, day, week, month, year, weekday

# Original Data Sources
Note that the actual data (in JSON) used in this project is a subset of original dataset preprocessed by the course. The provided data resides in AWS S3 (publically available).

1. Song data from Million Song Dataset
2. User activity data from Event Simulator based on Million Song Dataset

# Queries example

Top 5 Most Played Songs

%%sql
​
SELECT songplays.song_id, songs.title, COUNT(*) 
FROM songplays 
JOIN songs  
ON songplays.song_id = songs.song_id 
GROUP BY 1,2  
ORDER BY COUNT DESC 
LIMIT 5;
 * postgresql://awsuser:***@redshift-cluster-1.culufbgquc7t.us-east-1.redshift.amazonaws.com:5439/dev
5 rows affected.
song_id	title	count
SOCHRXB12A8AE48069	Let's Get It Started	3
SOFVOQL12A6D4F7456	The Boy With The Thorn In His Side	2
SOXQYSC12A6310E908	Bitter Sweet Symphony	2
SONQBUB12A6D4F8ED0	Angie (1993 Digital Remaster)	2
SOVWWJW12A670206BE	Astrud Astronette	1
Top 5 Most Used Browsers

%%sql
​
SELECT  user_agent, COUNT(*)
FROM songplays 
GROUP BY user_agent 
ORDER BY  COUNT DESC 
LIMIT 5;
 * postgresql://awsuser:***@redshift-cluster-1.culufbgquc7t.us-east-1.redshift.amazonaws.com:5439/dev
5 rows affected.
user_agent	count
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"	4
Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0	3
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"	2
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0	2
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"	1
Top 5 Most popular artist

%%sql
​
SELECT a.name, count(*)
FROM songplays p
JOIN artists a
ON p.artist_id = a.artist_id
GROUP BY 1
ORDER BY count DESC
LIMIT 5;
 * postgresql://awsuser:***@redshift-cluster-1.culufbgquc7t.us-east-1.redshift.amazonaws.com:5439/dev
5 rows affected.
name	count
Black Eyed Peas	3
The Verve	2
The Smiths	2
The Rolling Stones	2
Pearl Jam	1

