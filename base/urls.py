from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"), #the function to trigger 'home' which is defined in base/views.py
    path('room/<str:pk>/', views.room, name="room"), #pass functions since in this case we are using function based views hence 'room' function as argument passing in
    #<dynamic value> and str for stirng, or use int, or slug. pk:primarykey
    
    path('create-room/', views.createRoom, name="create-room")
]