from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..decorators import allowed_users
JWT_authenticator = JWTAuthentication()
from ..serializers import *
from ..models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['woreda'])
def getKebeleAdmins(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            woreda_name=request_user.woreda.woreda_name
            kbadmins = KebeleAdmin.objects.filter(created_by__woreda_name=woreda_name)
            serializer = KebeleAdminSerializer(kbadmins, many=True)
            return Response(serializer.data)
        except:
            return Response("something went wrong in the try block") 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['woreda'])
def createKebeleAdmins(request):
    data = request.data
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            woreda_id=request_user.woreda.id
            created_By=Woreda.objects.get(id=woreda_id)
            get_user=User.objects.filter(username=data['username'])
            if get_user:
                return Response("user already exists with this username")
            else:
                user= User.objects.create_user(username=data['username'],email=data['email'] ,password=data['password'])
                my_group = Group.objects.get(name='kebeleadmin')
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
                    kbadmin = KebeleAdmin.objects.create(
                        user=user,
                        kebele_name=data['kebele_name'],
                        created_by=created_By
                    )
                    pk=kbadmin.id
                    kb=KebeleAdmin.objects.get(id=pk)
                    serializer = KebeleAdminSerializer(kb, many=False)
                    return Response(serializer.data)
                else:
                    return Response("woreda creation failed")   
            
        except:
            return Response("something went wrong in the try block") 
    else:
        print("no token is provided in the header or the header is missing")

        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['woreda'])
def getkebeleadmin(request, pk):
    try:
        kebeleadmin = KebeleAdmin.objects.get(id=pk)
        serializer = KebeleAdminSerializer(kebeleadmin, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['woreda'])
def updateKebeleAdmin(request, pk):
    data = request.data
    kebeleAdmin = KebeleAdmin.objects.get(id=pk)
    serializer = KebeleAdminSerializer(instance=kebeleAdmin, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)

