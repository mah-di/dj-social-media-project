# Django Demo Social Media Project
Instagram inspired simple social media project built with Django.


## Introduction
This is a simple social media project built with django. This project is for learning purposes. I tried to implement the core concepts and functionalities of a social media platform.

Used Django template engine to build the frontend and default SQLite for database.


## Technologies used
- Django
- Celery
- Django Celery Results


## Setup
1. Download or clone the project in your desired location on your local machine
2. Create a virtual environtment - `virtualenv env`
3. Activate VirtualENV - ubuntu : `source env/bin/activate` || windows : `. env\Scripts\activate`
4. Run requirements.txt - `pip install -r requirements.txt` *(this will download and install all the required dependencies)*
5. Start development server - `python manage.py runserver`
6. Enter `localhost:8000` or `127.0.0.1:8000` on your browser to access the site


## Running Celery
- First you need to setup a message broker to communicate with Celery.
- After you've setup a message broker you need to update the `CELERY_BROKER_URL` as per your message broker URI on `settings.py` file.
- Run Celery server - ubuntu : `celery -A DjangoSocialMedia worker -l INFO` || windows : `celery -A DjangoSocialMedia worker -l info -P solo`
