# Library Management System (LMS)

A simple Flask-based Library Management System with user authentication, book management, and borrowing functionality.

---

## 📌 Features

- User registration and login
- Admin dashboard with:
  - Total books
  - Total users
  - Issued books
- Book management (Add/View books)
- Borrow and return books
- User dashboard to view borrowed books

---

## 🏗️ Architecture

Library_mgmt
│
├── app/
│ ├── models.py # Database models (User, Book, Borrow)
│ ├── routes.py # Flask routes and logic
│ ├── templates/ # HTML templates (Jinja2)
│ └── static/ # CSS, JS, images
├── config.py # Flask config
├── main.py # App entry point
└── requirements.txt # Dependencies


- **Database**: SQLite (`library.db`)
- **Authentication**: Flask-Login
- **Password Security**: Werkzeug password hashing

---

## ⚙️ Setup & Deployment

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd library_mgmt
2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application
python main.py


Visit http://127.0.0.1:5000
 in your browser.

🛠️ Admin Setup

To create an admin user manually:

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    admin = User(name="Admin", email="admin@example.com", password=generate_password_hash("admin123"), role="admin")
    db.session.add(admin)
    db.session.commit()


Login with admin credentials to access the Admin Dashboard.

## Default Admin Account

To access the admin dashboard, use the following credentials:

- **Email:** admin@example.com
- **Password:** admin123

> Note: You can log in as a normal user by registering through the website. (users can register themselves and only admin can add books.)