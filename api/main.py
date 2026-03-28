from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth-gateway.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class AuthView:
    @jwt_required
    def get_current_user(self):
        return get_jwt_identity()

    def login(self):
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
            return jsonify(access_token=access_token), 200
        return jsonify({'error': 'Invalid credentials'}), 401

    def register(self):
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({'error': 'Username already exists'}), 400
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return jsonify({'id': user.id, 'username': user.username}), 201

views = AuthView()

@app.route('/login', methods=['POST'])
def login():
    return views.login()

@app.route('/register', methods=['POST'])
def register():
    return views.register()

@app.route('/current_user', methods=['GET'])
def current_user():
    return views.get_current_user()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)