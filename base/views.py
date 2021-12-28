from django.contrib.auth import decorators
from django.http import request, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend developers'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    #if the user is logged in no option to further got to login
    #not through url on browser search top bar either
    #if prompted, it will be redirected to home page of that user

    if request.method == 'POST':
        username = request.POST.get('username').lower() 
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user) #log the user in which creates a session in the database and the browser and the user is redirected to home page
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context ={'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request) #deletes that session token hence logouts the user
    return redirect('home')


def registerPage(request):
    #page = 'register' # not needed since register shows up in the else statement in login_register.html
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            #commit=False: save the form and freezing it in time (the register) to execute the next statement
            # we want to be able to create the user right away to get that user object
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


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

    room_messages = Message.objects.filter(
        Q(room__name__icontains = q) |
        Q(room__topic__name__icontains = q) | #or parameter |
        Q(room__description__icontains = q) 
        )
    # OR
    # room_messages = Message.objects.filter(Q(room__topic__name__icontains = q) )

    context = {'rooms': rooms, 'topics': topics, 
                'room_count': room_count,
                'room_messages': room_messages} #context dictionary
    return render(request, 'base/home.html', context) 
    #any number of key:value pairs can be added here: 
    #'how we want to address it in the template: what we are passing in or here room dictionary defined on line 5
    # now we have access to this list on home.html


def room(request, pk):
    #when using the room dictionary instead of class
    # room = None 
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i

    #when using the room model
    room = Room.objects.get(id=pk) 
    #also argument should be something unique for checking in the database
    
    room_messages = room.message_set.all().order_by('-created')
    #in models.py class Message is child of class Room. 
    #This class Message is refferred in message_set.all but use lower case
    #now all messages of that particular room are in 'message'
    #no need to import Message class since parent element is being referred
    participants = room.participants.all()

    if request.method == 'POST':
        room_messages = Message.objects.create(
        #import Message model
            user = request.user,
            room = room,
            body = request.POST.get('body'), #reffered as body in room.html name=body
        )
        room.participants.add(request.user)
        #afterevery message the messager will be added as a partipant
        return redirect('room', pk=room.id)
        #without redirect itself the form will be in that page and the page will refresh but

    context = {'room': room, 'room_messages': room_messages,
                'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    # room_messages = Message.objects.get(user = user)
    topics = Topic.objects.all()
    #rooms will be used in feed_component.html, there we use for room in rooms
    #since this rooms will be passed to feed_component.html, it should have the same name as in feed_component
    context ={'user': user, 'rooms': rooms,
                'room_messages': room_messages,
                'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url = '/login') #decorator
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    page = 'Create'
    if request.method == 'POST':
        # print(request.POST)
        # to print the form input details on the bash terminal on submitting
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        #if the topic already exists, created=false and new topic is not created
        #if the topic already doesnt exist, created=true, and new topic will be created
        #form = RoomForm(request.POST) #creates a new form

        Room.objects.create(
            host = request.user,
            topic=topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        #create method is used because we are customizing the topic
        #and using the model form like below, is not quite easy

        # if form.is_valid():
        #     room = form.save(co mmit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
        #instead of the above line we could do 'request.POST.get('name')'
        # and manually get every field but since the ModelForm was made it will take care of this automatically


    context = {'form': form, 'topics': topics, 'page':page}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    page = 'Update'

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save(  )
        return redirect('home') #'home': name='home' in urls.py

    # if request.method == 'POST':
    #     form = RoomForm(request.POST, instance=room)
    #     #the instance=room is going to replace whatever value it was
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home') 

    context = {'form': form, 'topics': topics,
                 'page': page, 'room':room}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})
    #in delete.html obj is referred there, since we are deleting a room we pass room here
    # passing room will return the str method of room in models.py which returns the room name 


@login_required(login_url = '/login') #decorator
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect("'room' room.id")
    
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    # context={'form': form}
    return render(request, 'base/update-user.html', {'form': form})
