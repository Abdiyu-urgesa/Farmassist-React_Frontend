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
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebeleadmin'])
def getReports(request):
    response = JWT_authenticator.authenticate(request)
    request_user , token = response
    print(request_user)
    reports = Report.objects.filter(reported_to=request_user.id)
    serializer = ReportSerializer(reports, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebeleadmin','kebelebusiness'])
def createReport(request):
    data = request.data
    my_file = request.FILES.get('my_file')
    response = JWT_authenticator.authenticate(request)
    request_user , token = response
    user=User.objects.get(id=request_user.id)
    print(user)
    user_group=request.user.groups.all().first()
    print(user_group.name)
    if user_group.name=="kebele_admin":
        kb=KebeleAdmin.objects.get(user=user)
        to=kb.created_by
    if user_group.name=="woreda":
        kb=Woreda.objects.get(user=user)
        to=kb.created_by
    if user_group.name=="zone":
        kb=Zone.objects.get(user=user)
        to=kb.created_by
    else:
        kb=Region.objects.get(user=user)
        to=kb.created_by
    print(to)
    print(to)
    print(to)
    try:
        if my_file and to:
            resource = Report.objects.create(
                reported_by=request_user.id,
                reported_to=to,
                report_name=request.POST.get('report_name'),
                report_file=my_file
            )  
            print("dershalew\n")     
            _resource=Report.objects.get(id=resource.id)
            serializer = ReportSerializer(_resource, many=False)
            return Response(serializer.data)
        else:
            return Response("user not found")
    except Exception as e:
        return Response(e) 
      