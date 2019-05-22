# Turbot

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/python/black)
[![Maintainability](https://api.codeclimate.com/v1/badges/8a62b8af6f7a9eed396c/maintainability)](https://codeclimate.com/github/hugodelahousse/turbot/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/hugodelahousse/turbot/badge.svg?branch=master)](https://coveralls.io/github/hugodelahousse/turbot?branch=master)
[![Build Status](https://travis-ci.com/hugodelahousse/turbot.svg?branch=master)](https://travis-ci.com/hugodelahousse/turbot)


This repository uses [black](https://github.com/python/black) to check the coding style. You should probably
set it up as a pre-commit hook, like bellow:
```
$ pip install --user black
$ echo `black . >> .git/hooks/pre-commit`
```

To run this project, you need to set the appropriate env variables. You can do this easily with a `.env` file
```
$ cat .env
SLACK_API_TOKEN='<YOUR SLACK API TOKEN>'
ERROR_ICON_URL='https://i.imgur.com/Rt3XKCI.jpg'
SECRET_KEY='<LOCAL_SECRET_KEY>'
DJANGO_SETTINGS_MODULE=turbot.settings
PRAW_CLIENT_ID='<YOUR REDDIT CLIENT ID>'
PRAW_CLIENT_SECRET='<YOUR REDDIT CLIENT SECRET>'
DEBUG=True
PHOTO_FSTRING='<A FORMAT STRING TO SEND MEMBER PICTURES>'
SENTRY_DSN='<SENTRY DSN URL>'
```

To run the project locally, you can use the `docker-compose.yml` file as such:
```
$ docker-compose up -d
```
