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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getbardata(request):
    response = JWT_authenticator.authenticate(request)
    request_user , token = response

    combined_Data=[]
    regions = Region.objects.all()

    for region in regions:
        zones = Zone.objects.filter(created_by=region).count()
        print(zones)
        combined_Data.append({
            "region":region.Region_name,
            "zones":zones,
            "zonescolor": f"hsl({zones+5*10},70%,50%)"
        })



    serializer = BarSerializer(combined_Data, many=True)
    return Response(serializer.data)