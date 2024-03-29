from django.db import models

# Create your models here.

class FootballClub(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics/clubs')
    desc = models.TextField()
    price = models.IntegerField(default=0)
    is_club_in_city = models.BooleanField(default=False)


class Player(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics/players/')
    desc = models.TextField()
    country = models.TextField()
    price = models.IntegerField(default=0)