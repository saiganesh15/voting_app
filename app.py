from flask import Flask, render_template
import psycopg2
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# app = Flask(__name__, template_folder="templates", static_folder="static")
app = Flask(__name__)

op = ["India", "Pakistan", "Nepal", "Srilanka", "Afghanistan", "Bangladesh"]


@app.route("/")
def show_results():
    op = ["India", "Pakistan", "Nepal", "Srilanka", "Afghanistan", "Bangladesh"]

    def fetch_vote_counts():
        db_params = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "db",
            "port": "5432",
        }

        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Query to count votes for each option
        query = "SELECT vote, COUNT(*) FROM votes GROUP BY vote ORDER BY vote"
        cur.execute(query)

        total_votes = 0
        vote_data = []

        for row in cur:
            vote_option, count = row
            total_votes += count
            vote_data.append(
                {
                    "option": op[ord(vote_option) - ord('a')],
                    "count": count,
                }
            )

        cur.close()
        conn.close()

        return total_votes, vote_data

    def calculate_percentage(count, total):
        return round((count / total) * 100) if total != 0 else 0

    total_votes, vote_data = fetch_vote_counts()

    # Calculate percentages based on the corrected total_votes value
    for entry in vote_data:
        entry["percentage"] = calculate_percentage(entry["count"], total_votes)

    # Prepare data for rendering
    prepared_vote_data = []
    for country_name in op:
        index = next(
            (i for i, entry in enumerate(vote_data) if entry["option"] == country_name),
            None,
        )
        count = vote_data[index]["count"] if index is not None else 0
        prepared_vote_data.append(
            {
                "option": country_name,
                "count": count,
                "percentage": calculate_percentage(count, total_votes),
            }
        )

    sum_percentages = sum(entry["percentage"] for entry in prepared_vote_data)

    return render_template(
        "index.html",
        vote_data=prepared_vote_data,
        total_votes=total_votes,
        sum_percentages=sum_percentages,
        hostname=hostname,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, threaded=True)
