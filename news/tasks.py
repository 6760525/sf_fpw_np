from celery import shared_task
from .models import Post, Category
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives

@shared_task
def weekly_mail():
    week = datetime.now() - timedelta(days=7)
    cats = Category.objects.all()

    for cat in cats:
        weekly = Post.objects.filter(category = cat.id).filter(creation_time__date__gte=week)
        subscribers = cat.subscribers.all()
        emails = []

        for subscriber in subscribers:
            emails.append(subscriber.email)

        html_content = render_to_string('notification_weekly.html', {'weekly': weekly})

        msg = EmailMultiAlternatives(
            subject=f'Новости за неделю. Раздел: {cat} - {datetime.now().strftime("%Y-%m-%d")}',
            body='',
            from_email='aturin@yandex.ru',
            to=emails,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
