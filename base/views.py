from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# Dummy data for rooms
# rooms = [
#     {'id':1, 'name': 'Lets learn Python!'},
#     {'id':2, 'name': 'Design with me!'},
#     {'id':3, 'name': 'Frontend developers'},
# ]

def home(request):
    """Home Page View"""
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # Use Django's model manager to get all Rooms from DB
    # Use icontains to filter amd return results on partial search queries
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )
        
    topics = Topic.objects.all()
    # count() works faster than len()
    room_count = rooms.count()

    # context dict stores data sent to templates
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    """Room Pages View"""
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()

    # if the request is a POST request
    if request.method == 'POST':
        # save the POST data into the form
        form = RoomForm(request.POST)
        # if the form is valid, save to DB
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # prefill form with room details
    form = RoomForm(instance=room)

    # if we submit the form
    if request.method == 'POST':
        # save the new Room
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # if user confirms the delete, delete the room
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})