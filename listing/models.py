import pytz
from django.db import models
from datetime import datetime, timedelta

TAG_CHOICES = (
    ('0', 'Sale'),
    ('1', 'Wanted'),
)

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 200)
    url = models.CharField(max_length = 1000, unique=True)
    tag = models.CharField(max_length = 50, null=True)
    last_updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_past_due(self):
        tz = pytz.timezone('America/Los_Angeles')
        if datetime.now(tz) - timedelta(days=1) > self.last_updated_at:
            return True
        return False
