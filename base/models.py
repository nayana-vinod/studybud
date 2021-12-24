from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    # if Topic class was below Room class, then Topic should be specfied as models.FOreignKey('Topic, on_delete=models.SET_NULL, null=True)
    # a topic can have multiple rooms but a room can only have a single topic
    name = models.CharField(max_length=200)
    description =  models.TextField(null=True, blank=True) 
    #null=true means null value or no value for description is allowed in the databse
    #blank=true means like when it's saved like a form, the form can be blank
    # participants = 
    updated = models.DateTimeField(auto_now = True) 
    #every time the save stamp is clicked, it's gonna autosave the time and date
    created = models.DateTimeField(auto_now_add = True)
    #auto_now every time it is saved. auto_now_add saves only the first time it is being saved, the further saves won't affect this

    def __str__(self):
        return self.name 
        #should return a string ie if returned date do str(self.date_variable)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #one-to-many relationship since one user will have many messages
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True) 
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.body[0:50] #preview only first 50 characters in the admin panel