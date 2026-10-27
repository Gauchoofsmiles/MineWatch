
import sqlite3
from datetime import datetime
from collections import Counter

try:
    from flask import Flask, render_template  # type: ignore[import-not-found]
except ImportError:
    class Flask:
        def __init__(self, *args, **kwargs):
            pass

        def route(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator

    def render_template(*args, **kwargs):
        return ""

DB_NAME = 'risk.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS risk_overviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            risk_type TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            description TEXT,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_risk_overview(user, risk_type, risk_level, description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO risk_overviews (user, risk_type, risk_level, description, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (user, risk_type, risk_level, description, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_risk_overviews():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM risk_overviews ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows
app = Flask(__name__)

@app.route('/')
def show_risks():
        risks = get_all_risk_overviews()
        return render_template('risk.html', risks=risks)

if __name__ == '__main__':
        init_db()
        app.run(debug=True)
def get_risk_distribution():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT risk_type, risk_level FROM risk_overviews')
    risks = c.fetchall()
    conn.close()
    distribution = Counter(risks)
    return distribution

# Example usage:
if __name__ == '__main__':
    init_db()
    # add_risk_overview('alice', 'Financial', 'High', 'Potential loss due to market volatility')
    # add_risk_overview('bob', 'Operational', 'Medium', 'System downtime risk')
    print("All risk overviews:")
    for row in get_all_risk_overviews():
        print(row)
    print("\nRisk distribution:")
    for key, count in get_risk_distribution().items():
        print(f"{key}: {count}")