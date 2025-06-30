# 🏝️ YachtAway – Full-Stack Yacht Booking Platform

YachtAway is a luxury yacht booking application where users can:

- Browse beautiful yachts with images and descriptions
- Customize bookings with optional add-ons (e.g. DJ, chef, fishing gear)
- Register/login, view and edit bookings
- Track total pricing dynamically based on dates and options

Built with a **React frontend** and a **Flask + PostgreSQL backend**, it supports session-based authentication, image rendering, and responsive design.

---

## ⚙️ Tech Stack

| Frontend              | Backend                      | Database     | Other               |
|----------------------|------------------------------|--------------|---------------------|
| React (Vite)         | Flask (with Blueprints)      | PostgreSQL   | Flask-Migrate       |
| React Router         | Flask-SQLAlchemy             |              | Session Auth        |
| Custom CSS / Modules | RESTful API + MVC Structure  |              | Static Image Serving|

---


## 🧪 Features

✅ Register and login users  
✅ View and manage yacht bookings  
✅ Select add-ons with price calculation  
✅ Edit or cancel your bookings  
✅ View real yacht images stored locally  
✅ Session-based authentication (Flask session + cookies)

---

## 🧰 Setup Instructions

## BACKEND

## Navigate to the server directory**
 ```bash
cd server
 ```

## Create virtual env

```console
FLASK_APP=server.app:create_app
FLASK_ENV=development
```

## Install backend dependencies
```console
pipenv install
pipenv shell
```

## Run database migrations
```console
flask db init            
flask db migrate -m "Initial"
flask db upgrade
```

## Seed the database
```console
python -m server.seed
```

## Run the Flask
```console
flask run
```

## View the Database
```console
psql yachtaway_db
```

## Frontend (React + Vite)
Navigate to the client folder
```console
cd client
```

## Install frontend dependencies
```console
npm install
```

## Start the React app
```console
npm run dev
```

## 🔐 Authentication (Session-based)

## /auth/signup – POST
```console
{ "username": "mark",
 "email": "mark@mail.com", 
 "password": "abc123" }
```


## /auth/login – POST
```console
{ "username": "mark",
 "password": "abc123" }
```

## /auth/logout – DELETE
```console
Ends session and clears cookie.
```

## /auth/check_session – GET
```console
Verifies logged-in user.
```
