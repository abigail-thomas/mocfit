# mocfit+
This project will build a web-based fitness app that generates personalized workout plans from user profile data. By entering goals, experience level, and available equipment, users receive tailored exercise recommendations. The app helps people of all fitness levels structure routines without needing a trainer.

# Features
- User profile creation to personalize workout experience with goals avaliable equipment, and experience level
- Clean and responsive UI built with Tailwind + Flowbite components
- Authentication system using Django's built in user auth
- SQLite-backend database

# Tech Stack
## Frontend
- Tailwind CSS
- Flowbite (UI components)
- Bootstrap
- HTML, CSS, & JavaScript

## Backend
- Django
- SQLite (default local database)

## Ai Model
### Powered by Phi-3 (MIT Licensed) via Ollama


# Demo
add images here

# Installation
## 1. Clone the Repository
```
    git clone https://github.com/abigail-thomas/mocfit.git
    cd mocfit
```
## 2. Set Up Virtual Environment
```
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows
```
## 3. Install Python Dependencies
```
    pip install -r requirements.txt
```
## 4. Run Migrations
```
    python manage.py migrate
```
## 5. Start Development Server
```
    python manage.py runserver
```


# Configurations
Austin Heger
Joel Peters
Abigail Thomas
Maxwell Olson-Burkman