# Generated by Django 4.2.2 on 2023-07-02 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_profile', '0003_rename_last_name_profile_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='date_list', to='users_profile.profile'),
        ),
    ]