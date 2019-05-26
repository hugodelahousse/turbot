# Turbot

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/python/black)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/hugodelahousse/turbot.svg?style=for-the-badge)](https://codeclimate.com/github/hugodelahousse/turbot/maintainability)
[![Coverage](https://img.shields.io/coveralls/github/hugodelahousse/turbot.svg?style=for-the-badge)](https://coveralls.io/github/hugodelahousse/turbot?branch=master)
[![Build Status](https://img.shields.io/travis/com/hugodelahousse/turbot.svg?style=for-the-badge)](https://travis-ci.com/hugodelahousse/turbot)
[![Docker Build](https://img.shields.io/docker/cloud/build/hugodelahousse/turbot.svg?style=for-the-badge)](https://cloud.docker.com/repository/docker/hugodelahousse/turbot)
[![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/hugodelahousse/turbot.svg?style=for-the-badge)](https://cloud.docker.com/repository/docker/hugodelahousse/turbot/builds)


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
