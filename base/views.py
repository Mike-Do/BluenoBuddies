from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm

# Dummy data for rooms
# rooms = [
#     {'id':1, 'name': 'Lets learn Python!'},
#     {'id':2, 'name': 'Design with me!'},
#     {'id':3, 'name': 'Frontend developers'},
# ]

def loginPage(request):
    page = 'login'
    # restrict logged in users from accessing login page
    if request.user.is_authenticated:
        return redirect('home')

    # receiving a POST request to login
    if request.method == 'POST':    
        # make entered username case insensitive
        username = request.POST.get('username').lower()
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

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    # If user submitted the register form, process it
    if request.method == 'POST':
        # fill in form with user-entered data
        form = UserCreationForm(request.POST)
        # if form is valid
        if form.is_valid():
            # save user, commit=False in order to get access to user right away
            user = form.save(commit=False)
            # lowercase username in order to make sure usernames are consistent
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_register.html', {'form': form})

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
    
    # grab only the first five topics to display
    topics = Topic.objects.all()[0:5]
    # count() works faster than len()
    room_count = rooms.count()
    # messages for activity feed, only displays messages from current topic (i.e. q)
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    # context dict stores data sent to templates
    context = {'rooms': rooms, 'topics': topics, 
        'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    """Room Pages View"""
    room = Room.objects.get(id=pk)
    # query child objects of room, 'messege_set' --> gives us entire set of messages
    room_messages = room.message_set.all().order_by('-created')
    # get participants of a room
    participants = room.participants.all()

    # process submitted form for creating a message
    if request.method == 'POST':
        # fill in necessary fields from the Message model
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )

        # add as a new participant to the room
        room.participants.add(request.user)

        # fully reload page / make GET request
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages': room_messages, 
        'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)

    # get all of user's rooms for display in feed
    rooms = user.room_set.all()
    # get all messages of user
    room_messages = user.message_set.all()
    # grab all topics for Topic Browsing
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 
        'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

# redirect to login page if user is not logged in
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    # if the request is a POST request
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        # create topic
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
       
        return redirect('home')

    context = {'form': form, 'topics': topics}
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
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # update room info with update from submission
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'room': room}
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

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You do not have access to updating this room!')

    # if user confirms the delete, delete the room
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    # Render form
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    """View for Browse Topics Page"""
    # search GET request for topic search bar
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # get topics from DB related to search
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    """View for Activities Page (for mobile)"""
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
