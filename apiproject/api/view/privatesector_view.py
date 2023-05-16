from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from ..serializers import *
from ..models import *

@api_view(['GET'])
def getPrivateSectors(request):
    privates = PrivateSector.objects.all()
    serializer = PrivateSerializer(privates, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createPrivateSector(request):
    data = request.data
    try:
        user= User.objects.create_user(username=data['username'],email=data['email'] ,password=data['password'])
        my_group = Group.objects.get(name='privatesector')
        my_group.user_set.add(user)
        if user:
            privatesector = PrivateSector.objects.create(
                user=user,
                organization_name=data['organization_name'],
                tin_number=data['tin_number'] ,
                created_by=data['created_by'] )
            serializer = PrivateSerializer(privatesector, many=False)
            return Response(serializer.data)
        else:
            return Response("user creation failed")   
           
    except:
        return Response("something went wrong in the try block") 
        
@api_view(['GET'])
def getprivateSector(request, pk):
    try:
        privatesector = PrivateSector.objects.get(id=pk)
        serializer = PrivateSerializer(privatesector, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")

@api_view(['PUT'])
def updatePrivateSector(request, pk):
    data = request.data
    createPrivateSector = PrivateSector.objects.get(id=pk)
    serializer = PrivateSerializer(instance=createPrivateSector, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)

