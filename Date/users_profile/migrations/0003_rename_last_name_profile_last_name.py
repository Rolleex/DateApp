# Generated by Django 4.2.2 on 2023-07-02 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_profile', '0002_alter_profile_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Last_name',
            new_name='last_name',
        ),
    ]
