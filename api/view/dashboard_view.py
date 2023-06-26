from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..decorators import allowed_users
JWT_authenticator = JWTAuthentication()
from django.contrib.auth.models import User
from ..serializers import *
from ..models import *
import random


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getallUsersInDB(request):
    users = User.objects.all().count()
    return Response(users)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getbardata(request):
    response = JWT_authenticator.authenticate(request)
    request_user , token = response

    combined_Data=[]
    regions = Region.objects.all()

    for region in regions:
        zonesnum = Zone.objects.filter(created_by=region).count()
        zones = Zone.objects.filter(created_by=region)
        for zone in zones:
            woredasnum=Woreda.objects.filter(created_by=zone).count()
            woredas=Woreda.objects.filter(created_by=zone)
            for wereda in woredas:
                print("done3")
                
                kebeleAdminnum=KebeleAdmin.objects.filter(created_by=wereda).count()
                combined_Data.append({
                    "region":region.Region_name,
                    "zones":zonesnum,
                    "zonescolor": f"hsl({zonesnum+5*10},70%,50%)",
                    "woredas":woredasnum,
                    "woredascolor": f"hsl({woredasnum+13*6},70%,50%)",
                    "kebeleAdmin":kebeleAdminnum,
                    "kebeleAdmincolor": f"hsl({kebeleAdminnum+8*12},70%,50%)",
                })

    serializer = BarSerializer(combined_Data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def linedata(request):
    response = JWT_authenticator.authenticate(request)
    request_user, token = response
    combined_Data = []
    regions = Region.objects.all()
    for region in regions:
        print(region.Region_name)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        recource = Resource.objects.filter(user=region.user)
        if recource is not None:
            region_data = []  # Create a list to hold inner objects for this region
            for rec in recource:
                region_data.append({
                    "x": rec.name,
                    "y": rec.amount
                })
            combined_Data.append({
                "id": region.Region_name,
                "color": f"#{r:02x}{g:02x}{b:02x}",
                "data": region_data  # Append the inner object list to the outer list
            })
    return Response(combined_Data)
    
 

