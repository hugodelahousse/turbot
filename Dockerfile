FROM python:3

RUN pip install pipenv

WORKDIR /app
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex && pipenv install --deploy --system

COPY . /app

CMD python manage.py migrate

CMD gunicorn acu_bot.wsgi
