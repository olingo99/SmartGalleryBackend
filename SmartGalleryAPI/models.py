from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.

class Photo(models.Model):
    Path = models.CharField(max_length=200)
    Date = models.DateTimeField(auto_now=False, auto_now_add=True, blank= True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Persons = models.ManyToManyField('Person', through='LinkPhotoPerson')
    Tag = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.User} uploaded on {self.Date.date}'



class Person(models.Model):
    Name = models.CharField(max_length = 100)
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('Name', 'User')

    def __str__(self):
        return self.Name


class LinkPhotoPerson(models.Model):
    BoundingBox = models.CharField(max_length=100)
    Person = models.ForeignKey(Person, on_delete=models.CASCADE)
    Photo = models.ForeignKey(Photo,on_delete=models.CASCADE)

class CroppedFace(models.Model):
    Path = models.CharField(max_length=200)
    Person = models.ForeignKey(Person, on_delete=models.CASCADE)
    OriginalPhoto = models.ForeignKey(Photo, on_delete=models.CASCADE)