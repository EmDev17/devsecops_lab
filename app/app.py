from flask import Flask, request, jsonify, session
import sqlite3
import subprocess
import hashlib
import os
import yaml

app = Flask(__name__)

# VULN-1: Hardcoded secret key
app.secret_key = "supersecretkey123"

# VULN-2: Hardcoded database credentials
DB_HOST = "localhost"
DB_USER = "admin"
DB_PASS = "admin123"
DATABASE = "users.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            content TEXT
        )
    ''')
    # VULN-3: Weak password hashing (MD5)
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (1, 'admin', '{}', 'admin')".format(
            hashlib.md5("admin123".encode()).hexdigest()
        )
    )
    conn.commit()
    conn.close()

# VULN-4: SQL Injection
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(
        username, password_hash
    )
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    
    if user:
        session['user'] = username
        return jsonify({"message": "Login successful", "user": username})
    return jsonify({"message": "Invalid credentials"}), 401

# VULN-5: No input validation + SQL Injection
@app.route('/notes', methods=['POST'])
def add_note():
    user_id = request.form.get('user_id')
    content = request.form.get('content')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (user_id, content) VALUES ({}, '{}')".format(
        user_id, content
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Note added"})

@app.route('/notes/<user_id>', methods=['GET'])
def get_notes(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE user_id = {}".format(user_id))
    notes = cursor.fetchall()
    conn.close()
    return jsonify({"notes": notes})

# VULN-6: Command Injection
@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    result = subprocess.check_output("ping -c 1 " + host, shell=True)
    return jsonify({"result": result.decode()})

# VULN-7: Insecure YAML loading
@app.route('/config', methods=['POST'])
def load_config():
    data = request.data
    config = yaml.load(data, Loader=yaml.Loader)
    return jsonify({"config": str(config)})

# VULN-8: Sensitive data exposure
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify({"users": users})

if __name__ == '__main__':
    init_db()
    # VULN-9: Debug mode enabled in production
    app.run(debug=True, host='0.0.0.0', port=5000)
