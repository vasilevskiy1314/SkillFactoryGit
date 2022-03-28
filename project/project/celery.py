import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_every_30_seconds': {
        'task': 'news.tasks.weekly_mail_to_subs',
        'schedule': 30,
        'args': (),
    },
    'list_of_week_posts': {
        'task': 'news.tasks.list_of_week_posts',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}