from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from ..serializers import *
from ..models import *

@api_view(['GET'])
def getFarmerss(request):
    farmers = Farmer.objects.all()
    serializer = FarmerSerializer(farmers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createFarmer(request):
    data = request.data
    try:
        user= User.objects.create_user(username=data['username'],email=data['email'] ,password=data['password'])
        kebeleBusiness=KebeleBusiness.objects.get(id=data['created_by'])
        my_group = Group.objects.get(name='farmers')
        my_group.user_set.add(user)
        if user and kebeleBusiness:
            farmer = Farmer.objects.create(
                user=user,
                land_map_id=data['land_map_id'],
                land_size=data['land_size'],
                created_by=kebeleBusiness
              )
            serializer = FarmerSerializer(farmer, many=False)
            return Response(serializer.data)
        else:
            return Response("user creation failed")   
           
    except:
        return Response("something went wrong in the try block") 
        
@api_view(['GET'])
def getFarmer(request, pk):
    try:
        farmer = Farmer.objects.get(id=pk)
        serializer = FarmerSerializer(farmer, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
def updateFarmer(request, pk):
    data = request.data
    farmer = Farmer.objects.get(id=pk)
    serializer = FarmerSerializer(instance=farmer, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)

