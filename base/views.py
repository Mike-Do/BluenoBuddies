from django.shortcuts import render

# Dummy data for rooms
rooms = [
    {'id':1, 'name': 'Lets learn Python!'},
    {'id':2, 'name': 'Design with me!'},
    {'id':3, 'name': 'Frontend developers'},
]

def home(request):
    """Home Page View"""
    # context dict stores data sent to templates
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    """Room Pages View"""
    room = None

    # get the room with the respective pk from the rooms dict
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    
    context = {'room': room}
    return render(request, 'base/room.html', context)