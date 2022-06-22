from django.shortcuts import render
from .models import Room

# Dummy data for rooms
# rooms = [
#     {'id':1, 'name': 'Lets learn Python!'},
#     {'id':2, 'name': 'Design with me!'},
#     {'id':3, 'name': 'Frontend developers'},
# ]

def home(request):
    """Home Page View"""
    # Use Django's model manager to get all Rooms from DB
    rooms = Room.objects.all()
    # context dict stores data sent to templates
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    """Room Pages View"""
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)