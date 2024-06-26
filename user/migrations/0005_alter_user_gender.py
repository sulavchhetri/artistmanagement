# Generated by Django 5.0.6 on 2024-05-26 11:57

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', user.models.GenderEnum['MALE']), ('F', user.models.GenderEnum['FEMALE']), ('O', user.models.GenderEnum['OTHER'])], default=user.models.GenderEnum['MALE'], max_length=20),
        ),
    ]
