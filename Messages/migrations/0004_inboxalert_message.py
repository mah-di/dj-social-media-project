# Generated by Django 3.2.3 on 2021-06-08 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Messages', '0003_auto_20210609_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='inboxalert',
            name='message',
            field=models.CharField(default='', max_length=100),
        ),
    ]
