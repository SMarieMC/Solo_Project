# Generated by Django 2.2 on 2021-06-08 00:46

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('Solo_App', '0002_auto_20210607_1740'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Comment',
        ),
    ]
