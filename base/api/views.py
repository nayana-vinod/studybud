# from django.http import JsonResponse, response

from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer
from base.api import serializers

@api_view(['GET'])
# the http methods that are allowed to access this view
#that is this point this view can only take in GET requests
# @api_view(['GET', 'PUT', 'POST']) for allowing get, put, and post requests
def getRoutes(request):
    routes = [
        'GET /api/'
        #if you go to GET, you are going to get home page
        #users will know that because if they are viewing this then they'll be in the homepage
        'GET /api/rooms'
        'GET /api/rooms/:id'
    ]
    # python list of strings

    return Response(routes)

    # return JsonResponse(routes, safe=False)
    # safe: more than just python dictionaries can be used in routes/ or inside of this response
    # JsonResponse with safe=False will allow this list (routes) to be turned into a json list
    # and this json response is going to convert this data into json data


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    # first parameter: the object to be serialized
    #many: do we have multiple objects to serialize or one
    #here a query set 'rooms' is being serialized hence many=True

    return Response(serializer.data)
    #.data because not return the object but the data attribute
    #.data will give rooms in a serialzed format
    #this data can also be printed to see all the informtaion

    # return Response(rooms)
    #response: we are getting back a response 

#next feature: view/open a room and details in their website
@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    #gonna return a single object room with id=pk hence many=false

    return Response(serializer.data)
