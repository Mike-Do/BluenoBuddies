from dataclasses import field
from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        # get all fields from Room and autogenerate form
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
