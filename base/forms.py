from dataclasses import field
from django.forms import ModelForm
from .models import Room, User

class RoomForm(ModelForm):
    class Meta:
        # get all fields from Room and autogenerate form
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']