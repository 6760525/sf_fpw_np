import redis
from django.apps import AppConfig

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals
        from .views import BaseRegisterView
        from .tasks import weekly_mail
        from .scheduler import news_scheduler
        print('started!')

        news_scheduler.add_job(
            id='weekly_mail',
            func=weekly_mail,
            trigger='interval',
            seconds=300,
        )

        news_scheduler.start()
        
        
red = redis.Redis(
    host='redis-17971.c238.us-central1-2.gce.cloud.redislabs.com',
    port='17971',
    password='3VyoBGCtJYfYPPqaYVB0TfEjX4cLJ4kR'
    )