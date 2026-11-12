# Learnova – Collaborative Student Learning Platform

<p align="center">
  <img src="https://img.shields.io/badge/Django-6.x-green?style=for-the-badge&logo=django" />
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/MySQL-XAMPP-orange?style=for-the-badge&logo=mysql" />
  <img src="https://img.shields.io/badge/CSS-Custom-purple?style=for-the-badge" />
</p>

> **Learnova** is a full-stack collaborative learning platform where students discover topic-based study rooms, join communities, and discuss academic subjects — built with Django, MySQL, and a custom purple/blue UI.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Authentication | Register, Login, Logout with Django auth |
| 🏠 Study Rooms | Create, Edit, Delete, Join, Leave rooms |
| 🏷️ Topics | Filter rooms by topic (Python, ML, DSA, etc.) |
| 💬 Discussions | Real-time-style messaging inside rooms |
| 👤 Profiles | Custom bio, avatar, activity history |
| 🔍 Search | Full-text search across rooms and topics |
| 📊 Dashboard | Activity feed, popular topics, room stats |
| 📱 Responsive | Mobile-friendly custom CSS design |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.13, Django 6.x
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (no Bootstrap, no React)
- **Database:** MySQL via XAMPP
- **ORM:** Django ORM with PyMySQL adapter
- **Media:** Pillow for image handling

---

## 📁 Project Structure

```
Learnova/
├── config/              # Project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── __init__.py      # PyMySQL setup
├── core/                # Homepage & dashboard
│   ├── views.py
│   └── urls.py
├── accounts/            # Authentication & profiles
│   ├── models.py        # Profile model
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── signals.py
├── rooms/               # Study rooms & discussions
│   ├── models.py        # Room, Topic, Message, RoomMembership
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── core/home.html
│   ├── accounts/        # login, register, profile, edit_profile
│   └── rooms/           # room_list, room_detail, room_form, delete_room
├── static/
│   ├── css/style.css    # ~600 lines of custom CSS
│   └── js/script.js
├── media/               # Uploaded avatars
├── setup_db.py          # DB creation helper
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Run Instructions

### Prerequisites

- Python 3.10+
- XAMPP installed (for MySQL)
- Git (optional)

---

### Step 1 — Start XAMPP MySQL

1. Open **XAMPP Control Panel**
2. Click **Start** next to **MySQL**
3. Wait for the green status indicator

---

### Step 2 — Clone / Navigate to Project

```bash
cd path/to/Learnova
```

### Step 3 — Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
```

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Create the Database

```bash
python setup_db.py
```

This creates the `learnova_db` MySQL database automatically.

### Step 6 — Run Migrations

```bash
python manage.py migrate
```

### Step 7 — Create Admin (Optional)

```bash
python manage.py createsuperuser
```

### Step 8 — Start the Server

```bash
python manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000**

---

## 🗄️ Database Configuration

| Setting | Value |
|---|---|
| Engine | MySQL (via PyMySQL) |
| Database | `learnova_db` |
| Host | `localhost` |
| Port | `3306` |
| Username | `root` |
| Password | *(empty)* |

Configured in `config/settings.py`.

---

## 📸 Pages

| Page | URL |
|---|---|
| Homepage / Dashboard | `/` |
| All Study Rooms | `/rooms/` |
| Room Detail + Chat | `/rooms/<id>/` |
| Create Room | `/rooms/create/` |
| Edit Room | `/rooms/<id>/edit/` |
| Delete Room | `/rooms/<id>/delete/` |
| Join Room | `/rooms/<id>/join/` |
| Leave Room | `/rooms/<id>/leave/` |
| Register | `/accounts/register/` |
| Login | `/accounts/login/` |
| Logout | `/accounts/logout/` |
| Profile | `/accounts/profile/<username>/` |
| Edit Profile | `/accounts/profile/edit/me/` |
| Admin Panel | `/admin/` |

---

## 🎨 Design

- **Color Theme:** Purple (`#7c3aed`) + Blue (`#2563eb`)
- **Typography:** Inter (Google Fonts)
- **Layout:** CSS Grid — 3-column dashboard
- **Components:** Room cards, topic sidebar, activity feed, hero section
- **100% Custom CSS** — No Bootstrap, No Tailwind

---

## 🔒 Security

- CSRF protection on all forms
- Password hashing via Django's `auth`
- Login-required decorators on protected views
- Authorization checks (host-only edit/delete)
- Users can only delete their own messages

---

## 📄 License

MIT License — Free for personal and educational use.

---

<p align="center">Built with 💜 for students, by students | Learnova 2024</p>
