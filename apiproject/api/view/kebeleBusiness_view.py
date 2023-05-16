from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from ..serializers import *
from ..models import *

@api_view(['GET'])
def getKebeleBusiness(request):
    kebeleBusiness = KebeleBusiness.objects.all()
    serializer = KebeleBusinessSerializer(kebeleBusiness, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createKebeleBusiness(request):
    data = request.data
    try:
        user= User.objects.create_user(username=data['username'],email=data['email'] ,password=data['password'])
        kebeleadmin=KebeleAdmin.objects.get(id=data['created_by'])
        my_group = Group.objects.get(name='kebelebusiness')
        my_group.user_set.add(user)
        if user and kebeleadmin:
            kebeleBusiness = KebeleBusiness.objects.create(
                user=user,
                unique_name=data['unique_name'],
                created_by=kebeleadmin
              )
            serializer = KebeleBusinessSerializer(kebeleBusiness, many=False)
            return Response(serializer.data)
        else:
            return Response("user creation failed")   
           
    except:
        return Response("something went wrong in the try block") 
        
@api_view(['GET'])
def getKebeleBusines(request, pk):
    try:
        kebeleBusiness = KebeleBusiness.objects.get(id=pk)
        serializer = KebeleBusinessSerializer(kebeleBusiness, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
def updateKebeleBusiness(request, pk):
    data = request.data
    kebeleBusiness = KebeleBusiness.objects.get(id=pk)
    serializer = KebeleBusinessSerializer(instance=kebeleBusiness, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)

