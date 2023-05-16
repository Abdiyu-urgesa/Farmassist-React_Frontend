from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from ..serializers import *
from ..models import *

@api_view(['GET'])
def getKebeleAdmins(request):
    kebeleAdmins = KebeleAdmin.objects.all()
    serializer = KebeleAdminSerializer(kebeleAdmins, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createKebeleAdmins(request):
    data = request.data
    try:
        user= User.objects.create_user(username=data['username'],email=data['email'] ,password=data['password'])
        woreda=Woreda.objects.get(id=data['created_by'])
        my_group = Group.objects.get(name='kebeleadmin')
        my_group.user_set.add(user)
        if user and woreda:
            kebeleAdmin = KebeleAdmin.objects.create(
                user=user,
                kebele_name=data['kebele_name'],
                created_by=woreda
              )
            serializer = KebeleAdminSerializer(kebeleAdmin, many=False)
            return Response(serializer.data)
        else:
            return Response("user creation failed")   
           
    except:
        return Response("something went wrong in the try block") 
        
@api_view(['GET'])
def getkebeleadmin(request, pk):
    try:
        kebeleadmin = KebeleAdmin.objects.get(id=pk)
        serializer = KebeleAdminSerializer(kebeleadmin, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
def updateKebeleAdmin(request, pk):
    data = request.data
    kebeleAdmin = KebeleAdmin.objects.get(id=pk)
    serializer = KebeleAdminSerializer(instance=kebeleAdmin, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)

