# Generated by Django 5.1.1 on 2024-10-19 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='age',
        ),
    ]
