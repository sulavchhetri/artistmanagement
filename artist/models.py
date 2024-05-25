from django.db import models
from enum import Enum


class GenderEnum(Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class GenreEnum(Enum):
    RHYTHM_AND_BLUES = 'rnb'
    COUNTRY = 'country'
    CLASSIC = 'classic'
    ROCK = 'rock'
    JAZZ = 'jazz'


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=[(tag, tag.value) for tag in GenderEnum],
        default=GenderEnum.MALE
    )
    address = models.CharField(max_length=255)
    first_release_year = models.CharField(max_length=10)
    no_of_albums_released = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Music(models.Model):
    id = models.AutoField(primary_key=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    album_name = models.CharField(max_length=50)
    genre = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in GenreEnum])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
