from django.db import models
from workspaces.models import User, Channel
from django.conf import settings


class Submission(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=64)
    subreddit = models.CharField(max_length=64)
    title = models.CharField(max_length=256)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Deletes all old submissions
        # `delete()` does not support offsets
        old_submissions = Submission.objects.filter(channel=self.channel)\
            .order_by('-created_at')[settings.REDDIT_SUBMISSION_CACHE_COUNT:]
        Submission.objects.filter(pk__in=old_submissions).delete()


class Subscription(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    subreddit = models.CharField(max_length=128)

    class Meta:
        unique_together = ('channel', 'subreddit')

    def __str__(self):
        return f'Subscription<to `{self.subreddit}` in {self.channel}>'
