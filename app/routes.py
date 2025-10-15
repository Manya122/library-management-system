from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models import User, Book, Borrow
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

# ---------- HOME ----------
@main.route('/')
def home():
    return redirect(url_for('main.login'))

# ---------- AUTH ----------
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.user_dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        name = request.form.get('name', 'User')
        user = User(email=email, password=password, name=name, role='user')
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.login'))

# ---------- DASHBOARDS ----------
@main.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('main.user_dashboard'))

    books_count = Book.query.count()
    users_count = User.query.count()
    issued_books = Borrow.query.filter_by(returned=False).count()

    return render_template(
        'admin_dashboard.html',
        books_count=books_count,
        users_count=users_count,
        issued_books=issued_books
    )

@main.route('/user')
@login_required
def user_dashboard():
    borrowed_books = Borrow.query.filter_by(user_id=current_user.id, returned=False).all()
    return render_template(
        'user_dashboard.html',
        user_name=current_user.email.split('@')[0].capitalize(),
        borrowed_books=borrowed_books
    )

# ---------- BOOK MANAGEMENT ----------
@main.route('/books')
@login_required
def books():
    query = request.args.get('q', '')
    if query:
        books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
    else:
        books = Book.query.all()
    return render_template('books.html', books=books)

@main.route('/add_book', methods=['POST'])
@login_required
def add_book():
    if current_user.role == 'admin':
        title = request.form['title']
        author = request.form['author']
        category = request.form.get('category', 'General')
        new_book = Book(title=title, author=author, category=category, available=True)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
    return redirect(url_for('main.admin_dashboard'))

@main.route('/borrow/<int:book_id>')
@login_required
def borrow(book_id):
    book = Book.query.get(book_id)
    if book and book.available:
        book.available = False
        db.session.add(Borrow(user_id=current_user.id, book_id=book.id, returned=False))
        db.session.commit()
        flash('Book borrowed successfully!', 'success')
    else:
        flash('Book not available.', 'danger')
    return redirect(url_for('main.user_dashboard'))

@main.route('/return/<int:borrow_id>')
@login_required
def return_book(borrow_id):
    borrow = Borrow.query.get(borrow_id)
    if borrow and not borrow.returned:
        borrow.returned = True
        borrow.book.available = True
        db.session.commit()
        flash('Book returned successfully!', 'info')
    return redirect(url_for('main.user_dashboard'))
