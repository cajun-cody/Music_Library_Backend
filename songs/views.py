from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import SongSerializer
from .models import Song



# Create your views here.
@api_view(['GET','POST']) #Decorator to specify what requests can be made. 
def songs_list(request):
    if request.method == 'GET':
        songs = Song.objects.all() #Query to get all songs
        serializer = SongSerializer(songs,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SongSerializer(data=request.data) #Arguement the incoming request and accessing any data with that request.
        serializer.is_valid(raise_exception=True) #Statement to make sure data to POST is valid
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT', 'PATCH', 'DELETE'])
def songs_item(request, pk): #Adding pk will allow search for an object in the db by the primary key.
    song = get_object_or_404(Song, pk=pk) #Django shortcut to quary 
    if request.method == 'GET':
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = SongSerializer(song, data=request.data) #Arguement the incoming request and accessing any data with that request.
        serializer.is_valid(raise_exception=True) #Statement to make sure data to POST is valid
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        data = {'likes':song.likes + int(1)}
        serializer = SongSerializer(song, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


