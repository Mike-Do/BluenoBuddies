from django.shortcuts import render

# Create your views here.
def home(request):
    """Home Page View"""
    return render(request, 'home.html')

def room(request):
    """Home Page View"""
    return render(request, 'room.html')