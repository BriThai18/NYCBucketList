from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Event(models.Model):
    ACTIVITY = (
        ('Amusement Park', 'Amusement Park'),
        ('Hiking', 'Hiking'),
        ('Sight-seeing', 'Sight-seeing'),
        ('Restaurant', 'Restaurant'),
    )

    CITY = (
        ('Brooklyn', 'Brooklyn'),
        ('New York City', 'New York City'),
        ('Queens', 'Queens'),
        ('Bronx', 'Bronx'),
        ('Staten Island', 'Staten Island'),
    )

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    activity = models.CharField(max_length=200, null=True, choices=ACTIVITY)
    city = models.CharField(max_length=200, null=True, choices=CITY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True,  null=True)

    def __str__(self):
        return self.name

class Itinerary(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.event.title