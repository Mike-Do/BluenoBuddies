from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm

# Dummy data for rooms
# rooms = [
#     {'id':1, 'name': 'Lets learn Python!'},
#     {'id':2, 'name': 'Design with me!'},
#     {'id':3, 'name': 'Frontend developers'},
# ]

def loginPage(request):
    # receiving a POST request to login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if user exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        # authenticate() will error or return our user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # creates session in DB and browser
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password does not exist")

    context = {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

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

# redirect to login page if user is not logged in
@login_required(login_url='login')
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

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # prefill form with room details
    form = RoomForm(instance=room)

    # restrict users who are not hosts of room from updating it
    if request.user != room.host:
        return HttpResponse('You do not have access to updating this room!')

    # if we submit the form
    if request.method == 'POST':
        # save the new Room
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You do not have access to updating this room!')

    # if user confirms the delete, delete the room
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})