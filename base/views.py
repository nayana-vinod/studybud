from django.http import request
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend developers'},
# ]

def home(request): #pass in request object 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    #without the inline if statement and the below rooms statement when 'all' is given, no topics will be shown since q=None
    # rooms= Room.objects.filter(topic__name = q)

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | #or parameter |
        Q(name__icontains = q) |
        Q(description__icontains = q) 
        # Q(host__icontains = q) 
        )
    

    # rooms = Room.objects.all()
    topics = Topic.objects.all()
    room_count = rooms.count() #django method
    # or use len() method of python but count is faster

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count} #context dictionary
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
    form = RoomForm()
    if request.method == 'POST':
        # print(request.POST)
        # to print the form input details on the bash terminal on submitting
        form = RoomForm(request.POST) #creates a new form
        if form.is_valid():
            form.save()
            return redirect('home')
        #instead of the above line we could do 'request.POST.get('name')'
        # and manually get every field but since the ModelForm was made it will take care of this automatically


    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        #the instance=room is going to replace whatever value it was
        if form.is_valid():
            form.save()
            return redirect('home') #'home': name='home' in urls.py

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})
    #in delete.html obj is referred there, since we are deleting a room we pass room here
    # passing room will return the str method of room in models.py which returns the room name 