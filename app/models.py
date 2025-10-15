from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------------
# User Model
# -----------------------------
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), default="user")  # "admin" or "user"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    borrows = db.relationship('Borrow', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


# -----------------------------
# Book Model
# -----------------------------
class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    category = db.Column(db.String(100))
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    borrows = db.relationship('Borrow', backref='book', lazy=True)

    def __repr__(self):
        return f"<Book {self.title} | Available: {self.available}>"


# -----------------------------
# Borrow Model
# -----------------------------
class Borrow(db.Model):
    __tablename__ = 'borrow'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
    returned = db.Column(db.Boolean, default=False)
    returned_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Borrow User:{self.user_id} Book:{self.book_id} Returned:{self.returned}>"
