from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, User, Account, log_transaction
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Change this in production

db.init_app(app)
CORS(app)
jwt = JWTManager(app)

# Initialize database tables
with app.app_context():
    db.create_all()

### USER AUTHENTICATION ROUTES ###

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 400
    
    user = User(username=data['username'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login successful', 'token': access_token})
    
    return jsonify({'message': 'Invalid credentials'}), 401

### ACCOUNT ROUTES ###

@app.route('/create_account', methods=['POST'])
@jwt_required()
def create_account():
    user_id = get_jwt_identity()
    data = request.json
    new_account = Account(account_type=data['account_type'], balance=data.get('balance', 0), user_id=user_id)

    db.session.add(new_account)
    db.session.commit()
    return jsonify({'message': 'Account created successfully!', 'account_id': new_account.id})

@app.route('/get_accounts', methods=['GET'])
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    accounts = Account.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': acc.id, 'account_type': acc.account_type, 'balance': acc.balance} for acc in accounts])

### TRANSACTION ROUTES ###

@app.route('/deposit', methods=['POST'])
@jwt_required()
def deposit():
    data = request.json
    account = Account.query.get(data['account_id'])

    if not account:
        return jsonify({'message': 'Account not found'}), 404

    message = account.deposit(data['amount'])
    return jsonify({'message': message, 'new_balance': account.balance})

@app.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    data = request.json
    account = Account.query.get(data['account_id'])

    if not account:
        return jsonify({'message': 'Account not found'}), 404

    message = account.withdraw(data['amount'])
    return jsonify({'message': message, 'new_balance': account.balance})

@app.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    account_id = request.args.get('account_id')
    account = Account.query.get(account_id)

    if not account:
        return jsonify({'message': 'Account not found'}), 404

    transactions = account.transactions
    return jsonify([
        {
            "id": txn.id,
            "transaction_type": txn.transaction_type,
            "amount": txn.amount,
            "timestamp": txn.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for txn in transactions
    ])

if __name__ == "__main__":
    app.run(debug=True)
