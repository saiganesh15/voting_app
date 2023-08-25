from flask import Flask, render_template
import psycopg2
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# app = Flask(__name__, template_folder="templates", static_folder="static")
app = Flask(__name__)

@app.route('/')
def show_results():

    op = ["India", "Pakistan", "Nepal", "Srilanka", "Afghanistan", "Bangladesh"]
    def fetch_vote_counts():
        db_params = {
            'dbname': 'postgres',
            'user': 'postgres',
            'password': '3636',
            'host': 'localhost',
            'port': '5432'
        }

        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Query to count votes for each option
        query = "SELECT vote, COUNT(*) FROM votes GROUP BY vote ORDER BY vote"
        cur.execute(query)

        total_votes = 0
        vote_data = []  # List to store vote option data
        length_op = len(op)

        for row, country_name in zip(cur, op):
            vote_option, count = row
            total_votes += count
            vote_data.append({
                'option': country_name,
                'count': count,
            })

        cur.close()
        conn.close()

        return total_votes, vote_data

    def calculate_percentage(count, total):
        return round((count / total) * 100) if total != 0 else 0

    total_votes, vote_data = fetch_vote_counts()

# Calculate percentages based on the corrected total_votes value
    for entry in vote_data:
        entry['percentage'] = calculate_percentage(entry['count'], total_votes)

    # Calculate the sum of all vote percentages
    sum_percentages = sum(entry['percentage'] for entry in vote_data)

    # Printing the corrected vote data and sum of percentages
    print("Vote Results:")
    for entry in vote_data:
        print(f"Vote option: {entry['option']}, Count: {entry['count']}, Percentage: {entry['percentage']}%")

    print("Total Votes:", total_votes)
    print("Sum of Percentages:", sum_percentages)

    # Now you can access the corrected vote_data list and the sum_percentages value for future use.

    print("HELLOW WORLD")

    return render_template('index.html', vote_data=vote_data, total_votes=total_votes, sum_percentages=sum_percentages, hostname=hostname)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
