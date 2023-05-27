from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..decorators import allowed_users
JWT_authenticator = JWTAuthentication()
from ..serializers import *
from ..models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal'])
def getRegions(request):
    regions = Region.objects.all()
    serializer = RegionSerializer(regions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal'])
def createRegion(request):
    data = request.data
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            federal_id=request_user.federal.id
            created_By=Federal.objects.get(id=federal_id)
            # check if user already exsists
            get_user=User.objects.filter(username=data['username'])
            if get_user:
                return Response("user already exists with this username")
            else:
                user= User.objects.create_user(username=data['username'],email=data['email'] ,password=data['password'])
                my_group = Group.objects.get(name='region')
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
                    region = Region.objects.create(
                        user=user,
                        Region_name=data['region_name'],
                        created_by=created_By
                    )
                    pk=region.id
                    reg=Region.objects.get(id=pk)
                    serializer = RegionSerializer(reg, many=False)
                    return Response(serializer.data)
                else:
                    print("region creation failed")  
            
        except Exception:
            return Response(Exception) 
        
    else:
        print("no token is provided in the header or the header is missing")
   
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal'])
def getRegion(request, pk):
    try:
        region = Region.objects.get(id=pk)
        serializer = RegionSerializer(region, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal'])
def updatRegion(request, pk):
    data = request.data
    region = Region.objects.get(id=pk)
    serializer = RegionSerializer(instance=region, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        print("its me")
        return Response(serializer.errors)
    return Response(serializer.data)

