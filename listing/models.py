from django.db import models

TAG_CHOICES = (
    ('0', 'Sale'),
    ('1', 'Wanted'),
)

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 200)
    url = models.CharField(max_length = 1000, unique=True)
    tag = models.CharField(max_length=1, choices=TAG_CHOICES)
    last_updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
