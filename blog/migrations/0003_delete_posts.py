# Generated by Django 3.2.7 on 2021-10-09 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_change_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='img',
        ),
    ]