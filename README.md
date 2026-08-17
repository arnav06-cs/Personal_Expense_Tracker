# Personal Expense Tracker

A production-ready Expense Tracker built using:

- Python 3.12
- Django 5.1
- SQLite
- Bootstrap 5
- Chart.js
- ReportLab
- OpenPyXL

---

## Features

- User Authentication
- User Profile
- Expense CRUD
- Categories
- Search
- Filter
- Receipt Upload
- Monthly Reports
- Yearly Reports
- Budget Tracking
- Budget Warning
- PDF Export
- Excel Export
- Admin Panel
- Responsive UI

---

## Installation

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

Create database

```bash
python manage.py makemigrations

python manage.py migrate
```

Create admin

```bash
python manage.py createsuperuser
```

Run project

```bash
python manage.py runserver
```

Visit

```
http://127.0.0.1:8000
```

Admin

```
http://127.0.0.1:8000/admin
```

---

Developed for B.Tech Final Year Project.