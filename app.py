import datetime
import logging
import os
import time
from flask import Flask, redirect, render_template, request, make_response, g
import redis
import psycopg2
import socket
from psycopg2 import Error
import json  # Import JSON module to handle JSON data

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

# Replace with your PostgreSQL database connection details
db_host = "db"
db_name = "postgres"
db_user = "postgres"
db_password = "postgres"

# Replace with your Redis connection details
redis_host = "redis"
redis_port = 6379
redis_db = 0

# Initialize Redis client
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

print(f"Connecting to database: host={db_host}, name={db_name}, user={db_user}")
db = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

def perform_migration():
    print("Migration Sync is enabled!")
    while True:
        try:
            transfer_votes()
            # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format the timestamp
            # print("MIGRATION COMPLETE")
            # app.logger.info("Migration Synced")
        except Exception as e:
            print("Error during migration:", e)
        #time.sleep(2)  # Wait for 10 seconds before the next migration

def transfer_votes():
    # Retrieve votes from Redis and insert into PostgreSQL
    votes_data = redis_client.lrange('votes', 0, -1)
    db = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    try:      
        try:
            cursor = db.cursor()

            # Create the 'votes' table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS votes (
                    id SERIAL PRIMARY KEY,
                    voter_id VARCHAR(255),
                    vote VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT NOW()
                )
            """)

            db.commit()
            cursor.close()

        except Error as e:
            print("Error creating table/Table already exits:", e)


        cursor = db.cursor()

        # Truncate the table before inserting new data
        cursor.execute("TRUNCATE TABLE votes")
        db.commit()
        cursor.close()

        cursor = db.cursor()
        # Assuming the table structure is (voter_id TEXT, vote TEXT, timestamp TIMESTAMP)
        for vote_json in votes_data:
            vote_data = json.loads(vote_json.decode())  # Decode and load JSON data
            voter_id = vote_data['voter_id']
            vote = vote_data['vote']
            cursor.execute("INSERT INTO votes (voter_id, vote) VALUES (%s, %s)", (voter_id, vote))
        
        db.commit()
        cursor.close()
        db.close()

        message = "Votes transferred successfully!"
    except Error as e:
        message = f"Error transferring votes: {e}"
        print(e)  # Print the error for debugging

if __name__ == '__main__':
    perform_migration()

