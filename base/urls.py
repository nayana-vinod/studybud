from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name = "home"), #the function to trigger 'home' which is defined in base/views.py
    path('room/<str:pk>/', views.room, name="room"), #pass functions since in this case we are using function based views hence 'room' function as argument passing in
    #<dynamic value> and str for string, or use int, or slug. pk:primarykey
    # name can be used to mention the path here. this is useful since even if the url which is 'room/<str:pk>/' is changed it can be referenced using name='room'
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
] 