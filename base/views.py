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

def room(request):
    """Home Page View"""
    return render(request, 'base/room.html')