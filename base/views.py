from django.shortcuts import render
from .models import Room

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend developers'},
# ]

def home(request): #pass in request object 
    rooms = Room.objects.all()
    context = {'rooms': rooms} #context dictionary
    return render(request, 'base/home.html', context) 
    #any number of key:value pairs can be added here: 
    #'how we want to address it in the template: what we are passing in or here room dictionary defined on line 5
    # now we have access to this list on home.html

def room(request, pk):
    #when using the room dictionary
    # room = None 
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i

    #when using the room model
    room = Room.objects.get(id=pk) 
    #also argument should be something unique for checking in the database
    context = {'room': room}

    return render(request, 'base/room.html', context)

def createRoom(request):
    context = {}
    return render(request, 'base/room_form.html', context)