from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers import *
from ..decorators import allowed_users
JWT_authenticator = JWTAuthentication()
from ..models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebeleadmin'])
def getDAs(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            kebele_name=request_user.kebeleadmin.kebele_name
            das = DevelopmentalAgent.objects.filter(created_by__kebele_name=kebele_name)
            serializer = DASerializer(das, many=True)
            return Response(serializer.data)
        except:
            return Response("something went wrong in the try block") 



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebeleadmin'])
def createDA(request):
    data = request.data
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            kbadmin_id=request_user.kebeleadmin.id
            created_By=KebeleAdmin.objects.get(id=kbadmin_id)
            get_user=User.objects.filter(username=data['username'])
            if get_user:
                return Response("user already exists with this username")
            else:
                user= User.objects.create_user(username=data['username'],email=data['email'] ,password=data['password'])
                my_group = Group.objects.get(name='DA')
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
                    da = DevelopmentalAgent.objects.create(
                        user=user,
                        specialization=data['specialization'],
                        created_by=created_By
                    )
                    pk=da.id
                    kb=DevelopmentalAgent.objects.get(id=pk)
                    serializer = DASerializer(kb, many=False)
                    return Response(serializer.data)
                else:
                    return Response("Da creation failed")   
            
        except:
            return Response("something went wrong in the try block") 
   
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebeleadmin'])
def getDA(request, pk):
    try:
        DA = DevelopmentalAgent.objects.get(id=pk)
        serializer = DASerializer(DA, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebeleadmin'])
def updateDA(request, pk):
    data = request.data
    DA = DevelopmentalAgent.objects.get(id=pk)
    serializer = DASerializer(instance=DA, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)

