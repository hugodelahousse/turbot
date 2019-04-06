from django.db import models


class Team(models.Model):
    id = models.CharField(primary_key=True, db_index=True, max_length=30)
    domain = models.CharField(max_length=128, unique=True, db_index=True)


class Channel(models.Model):
    id = models.CharField(primary_key=True, db_index=True, max_length=30)
    name = models.CharField(max_length=128, db_index=True)
    team = models.ForeignKey(Team, related_name='channels', on_delete=models.CASCADE)

    @property
    def slack_channel(self):
        return f'<#{self.id}>'


class User(models.Model):
    id = models.CharField(primary_key=True, db_index=True, max_length=30)
    name = models.CharField(max_length=128, db_index=True)
    team = models.ForeignKey(Team, related_name='users', on_delete=models.CASCADE)

    @property
    def slack_username(self):
        return f'<@{self.id}>'
