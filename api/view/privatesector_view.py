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
@allowed_users(allowed_rolls=['kebelebusiness'])
def getPrivateSectors(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            privates = PrivateSector.objects.all()
            serializer = PrivateSerializer(privates, many=True)
            return Response(serializer.data)
        except:
            return Response("something went wrong in the try block") 
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebelebusiness'])
def createPrivateSector(request):
    data = request.data
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            kbbusiness_id=request_user.kebelebusiness.id
            created_By=KebeleBusiness.objects.get(id=kbbusiness_id)
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
                    privatesector = PrivateSector.objects.create(
                        user=user,
                        organization_name=data['organization_name'],
                        tin_number=data['tin_number'],
                        created_by=created_By
                    )
                    pk=privatesector.id
                    ps=PrivateSector.objects.get(id=pk)
                    serializer = PrivateSerializer(ps, many=False)
                    return Response(serializer.data)
                else:
                    return Response("KebeleAdmin creation failed")   
            
        except:
            return Response("something went wrong in the try block") 
    else:
        print("no token is provided in the header or the header is missing")

        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebelebusiness'])
def getprivateSector(request, pk):
    try:
        privatesector = PrivateSector.objects.get(id=pk)
        serializer = PrivateSerializer(privatesector, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebelebusiness'])
def updatePrivateSector(request, pk):
    data = request.data
    createPrivateSector = PrivateSector.objects.get(id=pk)
    serializer = PrivateSerializer(instance=createPrivateSector, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)

