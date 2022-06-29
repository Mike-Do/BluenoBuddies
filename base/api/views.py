from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer
from base.api import serializers

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api'
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]

    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    # because we are serializing a Query Set, we set many=True
    serializer = RoomSerializer(rooms, many=True)
    # accessing the data attribute gets us rooms in a serialized/JSON format
    return Response(serializer.data)