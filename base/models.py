from django.db import models
from django.contrib.auth.models import User



class Room(models.Model):
    #host = 
    #topic =
    name = models.CharField(max_length=200)
    # descriptions can be empty
    description = models.TextField(null=True, blank=True)
    # participants =
    # Updated and Created automatically set to current time
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class Message(models.Model):
    # use Django's User Model
    # one-to-many relationship (one user can have multiple messages)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # many-to-one relationship (many messages to one room)
    # CASCADE will get rid of all messages if room is deleted
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

    



