# Generated by Django 3.2.7 on 2021-10-10 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelTable(
            name='post',
            table='posts',
        ),
    ]