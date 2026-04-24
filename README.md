# 📔 Group6 Diary

A full-stack diary web application built with Django, deployed on PythonAnywhere. Users can write personal diary entries, follow friends, and interact through likes and comments.

🌐 **Live Demo**: [group6diary.pythonanywhere.com](https://group6diary.pythonanywhere.com)

---

## Features

- **Authentication** — Register, login, and logout securely
- **Diary Entries (CRUD)** — Create, read, update, and delete personal diary entries
- **Follow System** — Follow other users to see their diary entries in your feed
- **Like** — Like any diary entry from any user
- **Comments** — Comment on entries from users you mutually follow
- **User Profile** — Edit your username, bio, and profile picture
- **Search** — Search for other users by username
- **Pagination** — Feed displays 4 entries per page
- **Admin Panel** — Manage all data via Django admin interface

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13, Django 6.0 |
| Database | SQLite3 |
| Frontend | HTML, CSS, JavaScript |
| Deployment | PythonAnywhere |
| Version Control | Git, GitHub |

---

## Project Structure

```
group6Diary/
├── mysite/                  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── diaries/                 # Main application
│   ├── models.py            # DiaryEntry, Follow, Like, Comment, Profile
│   ├── views.py             # All view logic
│   ├── forms.py             # Django forms
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin configuration
│   ├── templates/
│   │   └── diaries/         # HTML templates
│   └── static/
│       └── diaries/
│           └── style.css    # Custom CSS
└── manage.py
```

---

## Database Models

- **DiaryEntry** — Stores diary entries with title, content, image, and timestamps
- **Follow** — Tracks follow relationships between users
- **Like** — Stores likes on diary entries
- **Comment** — Stores comments on diary entries (mutual followers only)
- **Profile** — Extends the default User model with bio and profile picture

---

## Getting Started (Local Setup)

**1. Clone the repository**
```bash
git clone https://github.com/Orlida/Django-Diary.git
cd Django-Diary
```

**2. Install dependencies**
```bash
pip install django pillow
```

**3. Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**4. Create a superuser**
```bash
python manage.py createsuperuser
```

**5. Run the development server**
```bash
python manage.py runserver
```

**6. Open your browser**
```
http://127.0.0.1:8000/
```

---

## Key Concepts Demonstrated

- **CRUD Operations** — Full create, read, update, delete for diary entries
- **User Authentication & Authorization** — Login required for all pages, users can only edit/delete their own entries
- **ORM (Object Relational Mapper)** — All database queries written in Python, no raw SQL
- **Django Templates** — Dynamic HTML rendering with template inheritance
- **Static & Media Files** — Custom CSS and user-uploaded images served correctly
- **Pagination** — Efficient data loading with Django's built-in Paginator
- **CSRF Protection** — All forms protected against Cross-Site Request Forgery

---

## Team

| Role | Responsibility |
|---|---|
| Frontend | HTML templates & CSS styling |
| Backend | Python, Django models, views, and deployment |

---

## License

This project was developed as a Chulalongkorn university coursework assignment.
