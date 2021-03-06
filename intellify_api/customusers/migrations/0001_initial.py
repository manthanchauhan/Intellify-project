# Generated by Django 2.2.8 on 2019-12-02 13:54

import customusers.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('name', models.CharField(max_length=40, validators=[customusers.validators.validate_name])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[customusers.validators.validate_phone], verbose_name='phone number')),
                ('user_name', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True, validators=[customusers.validators.validate_user_name])),
                ('password', models.CharField(max_length=300)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'user',
                'ordering': ['user_name'],
            },
        ),
    ]
