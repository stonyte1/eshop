# Instructions to run the initial application
- start the database `docker-compose up -d`
- create the virtual environment
- install dependencies `pip install requirements.txt`
- run migrations `python manage.py migrate`
- create super user `python manage.py createsuperuser`
- run server `python manage.py runserver` and enter admin site
- you can run interactive shell to play around with your models via `python manage.py shell`

