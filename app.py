from flask import Flask, request, jsonify
import psycopg2
from prometheus_client import start_http_server, Summary

app = Flask(__name__)

DB_CONFIG = {
    'host': 'db-server',  
    'database': 'flaskdb',
    'user': 'flaskuser',
    'password': 'flaskpass'
}

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@app.route('/')
def home():
    return "Hello from Flask with PostgreSQL backend!"

@app.route('/users')
@REQUEST_TIME.time()  
def users():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {'id': r[0], 'name': r[1], 'email': r[2]} for r in rows
        ])
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    start_http_server(8000)
    app.run(host="0.0.0.0", port=5000)
