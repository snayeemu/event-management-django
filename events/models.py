from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name 

class Event(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(default=date.today)
    time = models.TimeField() 
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, blank=True, null=True) 
    image = models.ImageField(upload_to="events_asset", default="events_asset/empty-image.jpg")

    def __str__(self):
        return self.name 

# class Participant(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     events = models.ManyToManyField(Event) 
