from flask import Flask, render_template, request
import redis
import psycopg2
from psycopg2 import Error
import json  # Import JSON module to handle JSON data

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
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
    
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)
