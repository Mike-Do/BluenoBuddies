from django.db import models

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

    



