# Generated by Django 3.2.9 on 2021-12-09 20:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restapi', '0002_rename_lessonbook_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='students',
            field=models.ManyToManyField(related_name='lessons', to=settings.AUTH_USER_MODEL),
        ),
    ]
