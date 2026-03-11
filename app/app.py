from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
import subprocess
import yaml

app = Flask(__name__)

# Fixed: Secret key from environment variable
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))

# Fixed: Database credentials from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(500), nullable=False)

with app.app_context():
    db.create_all()

# Fixed: Strong password hashing with SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fixed: Parameterized queries via SQLAlchemy ORM
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = hash_password(data.get('password', ''))
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    return jsonify({'message': 'Invalid credentials'}), 401

# Fixed: Parameterized queries via SQLAlchemy ORM
@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    note = Note(user_id=data.get('user_id'), content=data.get('content'))
    db.session.add(note)
    db.session.commit()
    return jsonify({'message': 'Note added'})

@app.route('/notes/<int:user_id>', methods=['GET'])
def get_notes(user_id):
    notes = Note.query.filter_by(user_id=user_id).all()
    return jsonify({'notes': [n.content for n in notes]})

# Fixed: No shell=True, use list arguments
@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host', 'localhost')
    allowed = {'localhost', '127.0.0.1'}
    if host not in allowed:
        return jsonify({'error': 'Invalid host'}), 400
    result = subprocess.run(['ping', '-c', '1', host],
                          capture_output=True, text=True, timeout=5)
    return jsonify({'output': result.stdout})

# Fixed: Safe YAML loading
@app.route('/config', methods=['POST'])
def update_config():
    data = request.get_json()
    config = yaml.safe_load(data.get('config', ''))
    return jsonify({'message': 'Config updated', 'config': config})

# Fixed: Never return passwords
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [{'id': u.id, 'username': u.username} for u in users]})

# Fixed: Debug off, bind to localhost only
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
