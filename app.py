from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User/Case model functions
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_lawyer = db.Column(db.Boolean, default=False)

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cases', lazy=True))

# Initialize the database itself
with app.app_context():
    db.create_all()

# Getting inputs from user
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_lawyer = data.get('is_lawyer', False)

    # Make sure user exists
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    # Create new user account
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, is_lawyer=is_lawyer)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User {username} created successfully!"}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    # Verify the password
    if user and check_password_hash(user.password, password):
        return jsonify({"message": f"Welcome, {username}!"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Creating the case itself
@app.route('/create_case', methods=['POST'])
def create_case():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    user_id = data.get('user_id')

    new_case = Case(title=title, description=description, user_id=user_id)
    db.session.add(new_case)
    db.session.commit()

    return jsonify({"message": f"Case '{title}' created successfully!"}), 201

# Getting the cases
@app.route('/cases', methods=['GET'])
def get_cases():
    cases = Case.query.all()
    case_list = [{"title": case.title, "description": case.description, "user_id": case.user_id} for case in cases]
    return jsonify(case_list), 200

# Getting the lawyers
@app.route('/lawyers', methods=['GET'])
def get_lawyers():
    lawyers = User.query.filter_by(is_lawyer=True).all()
    lawyer_list = [{"username": lawyer.username, "id": lawyer.id} for lawyer in lawyers]
    return jsonify(lawyer_list), 200

if __name__ == '__main__':
    app.run(debug=True)
