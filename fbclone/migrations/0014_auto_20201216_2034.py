# Generated by Django 3.0.3 on 2020-12-16 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fbclone', '0013_friend_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='id',
        ),
        migrations.AlterField(
            model_name='friend',
            name='chat',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
