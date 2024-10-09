import os
import psycopg2
import datetime
from dotenv import load_dotenv
from sql_queries import copy_table_queries, insert_table_queries

# Load environment variables from the .env file
load_dotenv()

def load_staging_tables(cur, conn):
    """
    This function copies data from S3 into staging tables in Redshift cluster.

    :param cur: Database cursor reference
    :param conn: Database connection instance
    :return: None
    """
    total_queries = len(copy_table_queries)
    print(f"There are {total_queries} tables to load")

    for idx, query in enumerate(copy_table_queries):
        print(f"Loading table: {idx + 1}/{total_queries}")
        print(f"{query}")

        start_time = datetime.datetime.now()
        cur.execute(query)
        conn.commit()

        print("Loading took: {millisec} ms.".format(
            millisec=(datetime.datetime.now() - start_time).microseconds / 1000.0
        ))

def insert_tables(cur, conn):
    """
    This function runs all `INSERT INTO TABLE` queries to insert data from the staging tables into 
    dimensional and fact tables in Redshift cluster.

    :param cur: Database cursor reference
    :param conn: Database connection instance
    :return: None
    """
    total_queries = len(insert_table_queries)
    print(f"There are {total_queries} tables to insert")

    for idx, query in enumerate(insert_table_queries):
        print(f"Inserting table: {idx + 1}/{total_queries}")
        print(f"{query}")

        start_time = datetime.datetime.now()
        cur.execute(query)
        conn.commit()

        print("Loading took: {millisec} ms.".format(
            millisec=(datetime.datetime.now() - start_time).microseconds / 1000.0
        ))

def main():
    # Retrieve environment variables for database connection
    host = os.getenv('HOST')
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    port = os.getenv('DB_PORT')

    print("Connecting to Redshift...")
    
    # Establish connection to Redshift using environment variables
    conn = psycopg2.connect(f"host={host} dbname={dbname} user={user} password={password} port={port}")
    cur = conn.cursor()

    print("Start loading S3 to Staging tables...")
    load_staging_tables(cur, conn)

    print("Start loading Staging tables to Production tables...")
    insert_tables(cur, conn)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
