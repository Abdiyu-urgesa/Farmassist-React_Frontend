from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from ..serializers import *
from ..models import *

@api_view(['GET'])
def getAnnouncement(request):
    announcement = Announcement.objects.all()
    serializer = AnnouncementSerializer(announcement, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createAnnouncement(request):
    data = request.data
    try:
        announcement = Announcement.objects.create(
            sent_by=data['sent_by'],
            title=data['title'],
            discription=data['discription'],
            to=User.objects.get(id= data['to'])
        )       
        serializer = AnnouncementSerializer(announcement, many=False)
        return Response(serializer.data)
    
    except:
        return Response("something went wrong in the try block") 
        
@api_view(['GET'])
def getAnnouncement(request, pk):
    try:
        announcement = Announcement.objects.get(id=pk)
        serializer = AnnouncementSerializer(announcement, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
def updateAnnouncement(request, pk):
    data = request.data
    announcement = Announcement.objects.get(id=pk)
    serializer = AnnouncementSerializer(instance=announcement, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)

