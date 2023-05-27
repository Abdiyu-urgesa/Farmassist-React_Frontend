from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..decorators import allowed_users
JWT_authenticator = JWTAuthentication()
from ..serializers import *
from ..models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['region'])
def getZones(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            region_name=request_user.region.Region_name
            zones = Zone.objects.filter(created_by__Region_name=region_name)
            serializer = ZoneSerializer(zones, many=True)
            return Response(serializer.data)
        except:
            return Response("something went wrong in the try block") 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['region'])
def createZone(request):
    data = request.data
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            region_id=request_user.region.id
            created_By=Region.objects.get(id=region_id)
            # check if user already exsists
            get_user=User.objects.filter(username=data['username'])
            if get_user:
                return Response("user already exists with this username")
            else:
                user= User.objects.create_user(username=data['username'],email=data['email'] ,password=data['password'])
                my_group = Group.objects.get(name='zone')
                my_group.user_set.add(user)
                if user and created_By:
                    UserProfile.objects.create(
                    user=user,
                    fname=data['fname'],
                    Mname = data['Mname'],
                    lname =data['lname'],
                    phone =data['phone'],
                    sex =data['sex'],
                    profile =data['profile']
                    )
                    zone = Zone.objects.create(
                        user=user,
                        Zone_name=data['Zone_name'],
                        created_by=created_By
                    )
                    pk=zone.id
                    zn=Zone.objects.get(id=pk)
                    serializer = ZoneSerializer(zn, many=False)
                    return Response(serializer.data)
                else:
                    return Response("user creation failed")   
            
        except:
            return Response("something went wrong in the try block") 
    else:
        print("no token is provided in the header or the header is missing")
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['region'])
def getZone(request, pk):
    try:
        zone = Zone.objects.get(id=pk)
        serializer = ZoneSerializer(zone, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['region'])
def updatZone(request, pk):
    data = request.data
    zone = Zone.objects.get(id=pk)
    serializer = ZoneSerializer(instance=zone, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)

