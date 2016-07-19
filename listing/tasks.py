import uuid
import pytz

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from scrapinghub import Connection
from django.conf import settings
from listing.models import Post
from datetime import datetime
 
logger = get_task_logger(__name__)
 
# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def fetch_hourly():
    logger.info("Start task")
    conn = Connection(settings.SCRAPINGHUB_KEY)
    project = conn[65427]
    jobs = project.jobs(state='finished', has_tags='hourly', count=2)
    for job in jobs:
        saveItems(job.items())

def saveItems(res):
    for entry in res:
        link = str(entry['link'])
        link_hash = uuid.uuid3(uuid.NAMESPACE_DNS, link)
        updated_values = {'url': link, 'tag': entry['tag'], 'title': entry['title'], 'last_updated_at': parseTime(entry['timestamp'])}
        p, created = Post.objects.update_or_create(url_index=link_hash, defaults=updated_values)

# time_string is expected as 2016-05-17
def parseTime(time_string):
    tz = pytz.timezone('America/Los_Angeles')
    try:
        return tz.localize(datetime.strptime(time_string, "%Y-%m-%d"))
    except ValueError:
        format = '%Y-%m-%d %I:%M %p'
        try:
          return tz.localize(datetime.strptime(time_string, format))
        except ValueError:
          return datetime.now(tz)
