from django.shortcuts import render

# Dummy data for rooms
rooms = [
    {'id':1, 'name':'Lets learn Python!'}
    {'id':2, 'name':'Design with me!'}
    {'id':3, 'name':'Frontend developers'}
]

def home(request):
    """Home Page View"""
    return render(request, 'home.html')

def room(request):
    """Home Page View"""
    return render(request, 'room.html')