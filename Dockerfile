FROM python:3

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN set -ex && pipenv install --deploy --system

COPY . /app

CMD gunicorn turbot.wsgi
