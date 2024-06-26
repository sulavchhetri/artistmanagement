# Generated by Django 5.0.6 on 2024-05-26 12:02

import artist.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0002_alter_artist_no_of_albums_released'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='gender',
            field=models.CharField(choices=[('M', artist.models.GenderEnum['MALE']), ('F', artist.models.GenderEnum['FEMALE']), ('O', artist.models.GenderEnum['OTHER'])], default=artist.models.GenderEnum['MALE'], max_length=20),
        ),
        migrations.AlterField(
            model_name='music',
            name='genre',
            field=models.CharField(choices=[('rnb', artist.models.GenreEnum['RHYTHM_AND_BLUES']), ('country', artist.models.GenreEnum['COUNTRY']), ('classic', artist.models.GenreEnum['CLASSIC']), ('rock', artist.models.GenreEnum['ROCK']), ('jazz', artist.models.GenreEnum['JAZZ'])], max_length=20),
        ),
    ]
