from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    """Parent model to Rooms"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Set topic of room to Null if topic is deleted
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    # descriptions can be empty
    description = models.TextField(null=True, blank=True)
    # participants is a many-to-many relationship (many users, many rooms)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    # Updated and Created automatically set to current time
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # orders rooms by most updated at top
        ordering = ['-updated', '-created']


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

    class Meta:
        # orders messages by most updated at top of Activity Feed
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]