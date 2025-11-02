# 💸 Truly Expenses – Django Expense Management System

**Truly Expenses** is a web-based application built using Django that allows users to manage, track, and visualize their daily expenses with ease. This system provides a simple interface to add transactions, categorize expenses, view daily/monthly summaries, and manage budgets — all securely and efficiently.

## 🌐 Live Demo

➡️ [Visit Live Application](https://expense-tracker-zn1o.onrender.com/)  
🚀 Deployed using Render

---

## 📌 Features

- User Registration & Authentication
- Add/Edit/Delete Transactions
- Categorize Expenses (Food, Bills, Travel, etc.)
- View Total Expenses per Day/Month
- Responsive UI with Bootstrap
- Secure CRUD operations with CSRF protection
- SQLite database (PostgreSQL planned for future deployment)
- Admin Panel for backend management

---

## 🧰 Technologies Used

- **Backend**: Django (Python 3)
- **Frontend**: HTML5, CSS3, Bootstrap
- **Database**: SQLite (development), PostgreSQL (planned)
- **Deployment**: Render
- **Version Control**: Git & GitHub

---

## 🛠️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate



pip install -r requirements.txt



python manage.py migrate



python manage.py runserver
