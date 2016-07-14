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
    url = models.CharField(max_length = 500)
    url_index = models.UUIDField(unique=True, editable=False)
    tag = models.CharField(max_length = 50, null=True)
    last_updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_past_due(self):
        tz = pytz.timezone('America/Los_Angeles')
        if datetime.now(tz) - timedelta(days=1) > self.last_updated_at:
            return True
        return False

    @property
    def is_only_date(self):
        return self.last_updated_at.hour == 7 and self.last_updated_at.minute == 0 and self.last_updated_at.second == 0
