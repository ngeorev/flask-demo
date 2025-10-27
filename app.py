from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    'host': 'db-server', 
    'database': 'flaskdb',
    'user': 'flaskuser',
    'password': 'flaskpass'
}

@app.route('/')
def home():
    return "Hello from Flask with PostgreSQL backend!"

@app.route('/users')
def users():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({'db_version': version[0]})
    except Exception as e:
        return jsonify({'error': str(e)})
