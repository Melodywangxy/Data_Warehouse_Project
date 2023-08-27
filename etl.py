import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """This function is to copy S3 data into staging tables on redshift"""
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """This function is to insert data from staging tables into analytic tables"""
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """This function is to establish connection to redshift database, call
    functions to load staging tables from S3 and copy staged data into 
    analytic tables. Close connection in the end.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
