# Generated by Django 4.2.2 on 2023-07-03 00:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_profile', '0005_profile_latitude_profile_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=8, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
        ),
    ]
