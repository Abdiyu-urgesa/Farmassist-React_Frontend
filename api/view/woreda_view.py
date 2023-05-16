from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from ..serializers import *
from ..models import *

@api_view(['GET'])
def getWeredas(request):
    woreda = Woreda.objects.all()
    serializer = WoredaSerializer(woreda, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createWoreda(request):
    data = request.data
    try:
        user= User.objects.create_user(username=data['username'],email=data['email'] ,password=data['password'])
        zone=Zone.objects.get(id=data['created_by'])
        my_group = Group.objects.get(name='woreda')
        my_group.user_set.add(user)
        if user and zone:
            woreda = Woreda.objects.create(
                user=user,
                woreda_name=data['woreda_name'],
                created_by=zone
              )
            serializer = WoredaSerializer(woreda, many=False)
            return Response(serializer.data)
        else:
            return Response("user creation failed")   
           
    except:
        return Response("something went wrong in the try block") 
        
@api_view(['GET'])
def getWoreda(request, pk):
    try:
        woreda = Woreda.objects.get(id=pk)
        serializer = WoredaSerializer(woreda, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
def updateWoreda(request, pk):
    data = request.data
    woreda = Woreda.objects.get(id=pk)
    serializer = WoredaSerializer(instance=woreda, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)
