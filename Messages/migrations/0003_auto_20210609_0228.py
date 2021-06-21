# Generated by Django 3.2.3 on 2021-06-08 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Messages', '0002_auto_20210609_0101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='alert',
        ),
        migrations.CreateModel(
            name='InboxAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert', models.BooleanField(default=True)),
                ('last_alert', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_from', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-last_alert',),
            },
        ),
    ]