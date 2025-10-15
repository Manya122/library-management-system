from app import create_app, db
from app.models import User, Book
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # --- Add Users ---
    if not User.query.first():  # Only add if DB empty
        admin = User(
            name="Admin User",
            email="admin@example.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )
        user = User(
            name="Normal User",
            email="user@example.com",
            password=generate_password_hash("user123"),
            role="user"
        )
        author = User(
            name="Author User",
            email="author@example.com",
            password=generate_password_hash("author123"),
            role="author"
        )
        db.session.add_all([admin, user, author])
        db.session.commit()
        print("Users added: Admin, User, Author")

    # --- Add Sample Books ---
    if not Book.query.first():  # Only add if DB empty
        books = [
            Book(title="The Alchemist", author="Paulo Coelho", category="Fiction"),
            Book(title="1984", author="George Orwell", category="Dystopian"),
            Book(title="Clean Code", author="Robert C. Martin", category="Programming"),
            Book(title="Harry Potter and the Sorcerer's Stone", author="J.K. Rowling", category="Fantasy"),
            Book(title="To Kill a Mockingbird", author="Harper Lee", category="Classic"),
        ]
        db.session.bulk_save_objects(books)
        db.session.commit()
        print("Sample books added!")
