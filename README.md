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

# queries example
