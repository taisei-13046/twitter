# Generated by Django 3.2.7 on 2021-10-07 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_post_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='author',
        ),
    ]
