from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True)

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password is correct."""
        return bcrypt.check_password_hash(self.password, password)


class Account(db.Model):
    """Account model representing user bank accounts."""
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(50), nullable=False)  # Savings, Checking, etc.
    balance = db.Column(db.Float, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def deposit(self, amount):
        """Deposits money into the account and logs the transaction."""
        if amount > 0:
            self.balance += amount
            log_transaction(self.id, "deposit", amount)
            db.session.commit()
            return f"Deposited ${amount}. New balance: ${self.balance}"
        return "Invalid deposit amount."

    def withdraw(self, amount):
        """Withdraws money from the account if funds are sufficient."""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            log_transaction(self.id, "withdrawal", amount)
            db.session.commit()
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        return "Insufficient funds or invalid withdrawal amount."


class Transaction(db.Model):
    """Model for transaction history."""
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # deposit, withdrawal
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Transaction {self.transaction_type} ${self.amount} on {self.timestamp}>"


# Function to log transactions
def log_transaction(account_id, transaction_type, amount):
    """Logs a deposit or withdrawal transaction."""
    transaction = Transaction(account_id=account_id, transaction_type=transaction_type, amount=amount)
    db.session.add(transaction)
    db.session.commit()
