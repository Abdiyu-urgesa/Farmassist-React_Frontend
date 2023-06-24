from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from ..decorators import allowed_users
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers import *
from ..models import *

JWT_authenticator = JWTAuthentication()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal'])
def getFederals(request):
    federals = Federal.objects.all()
    serializer = FederalSerializer(federals, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal'])
def createFederal(request):
    data = request.data
    try:
        get_user=User.objects.filter(username=data['username'])
        if get_user:
            return Response("user already exsist with this username")
        else:
            user= User.objects.create_user(username=data['username'],email=data['email'] ,password=data['password'])
            my_group = Group.objects.get(name='federal')
            my_group.user_set.add(user)
            if user:
                UserProfile.objects.create(
                    user=user,
                    fname=data['fname'],
                    Mname = data['Mname'],
                    lname =data['lname'],
                    phone =data['phone'],
                    sex =data['sex'],
                    profile =data['profile']

                )
                federal = Federal.objects.create(
                    user=user,
                    Federal_name=data['Federal_name'],
                )
                serializer = FederalSerializer(federal, many=False)
                return Response(serializer.data)
            else:
                return Response("user creation failed")   
            
    except Exception as e:
        return Response(e) 
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal'])
def getFederal(request, pk):
    try:
        federal = Federal.objects.get(id=pk)
        serializer = FederalSerializer(federal, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal'])
def updatFederal(request, pk):
    data = request.data
    federal = Federal.objects.get(id=pk)
    serializer = FederalSerializer(instance=federal, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)

