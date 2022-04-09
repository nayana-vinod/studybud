from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.deletion import CASCADE

from django.contrib.auth.models import AbstractUser
#
# Create your models here.


#django to look at the new abstract user isntead of what we already had
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    #no blank=true: this is a requiired field
    email = models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =[]


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    # if Topic class was below Room class, then Topic should be specfied as models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
    # a topic can have multiple rooms but a room can only have a single topic
    name = models.CharField(max_length=200)
    description =  models.TextField(null=True, blank=True) 
    #null=true means null value or no value for description is allowed in the databse
    #blank=true means like when it's saved like a form, the form can be blank
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    #since host used User, another attribute using it needs related_name
    updated = models.DateTimeField(auto_now = True) 
    #every time the save stamp is clicked, it's gonna autosave the time and date
    created = models.DateTimeField(auto_now_add = True)
    #auto_now every time it is saved. auto_now_add saves only the first time it is being saved, the further saves won't affect this


    class Meta:
        # ordering can also be specified as a query like in the attribute of Room class
        ordering = ['-updated', '-created']
        # without the - ie if ordering = ['updated', 'created'] this will create it in ascending order that is updated or created last will be lst like it is already

    def __str__(self):
        return self.name 
        #should return a string ie if returned date do str(self.date_variable)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #one-to-many relationship since one user will have many messages
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True) 
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50] #preview only first 50 characters in the admin panel