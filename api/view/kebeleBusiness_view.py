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
def getKebeleBusiness(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            kebele_name=request_user.kebeleadmin.kebele_name
            kebeleBusiness = KebeleBusiness.objects.filter(created_by__kebele_name=kebele_name)
            serializer = KebeleBusinessSerializer(kebeleBusiness, many=True)
            return Response(serializer.data)
        except:
            return Response("something went wrong in the try block") 



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebeleadmin'])
def createKebeleBusiness(request):
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
                my_group = Group.objects.get(name='kebelebusiness')
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
                    kbbusiness = KebeleBusiness.objects.create(
                        user=user,
                        unique_name=data['unique_name'],
                        created_by=created_By
                    )
                    pk=kbbusiness.id
                    kb=KebeleBusiness.objects.get(id=pk)
                    serializer = KebeleBusinessSerializer(kb, many=False)
                    return Response(serializer.data)
                else:
                    return Response("woreda creation failed")   
            
        except:
            return Response("something went wrong in the try block") 
   
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebeleadmin'])
def getKebeleBusines(request, pk):
    try:
        kebeleBusiness = KebeleBusiness.objects.get(id=pk)
        serializer = KebeleBusinessSerializer(kebeleBusiness, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebeleadmin'])
def updateKebeleBusiness(request, pk):
    data = request.data
    kebeleBusiness = KebeleBusiness.objects.get(id=pk)
    serializer = KebeleBusinessSerializer(instance=kebeleBusiness, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebelebusiness'])
def GetRecourceToDistribute(request):
    data = request.data
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            kb_id=request_user.kebelebusiness.id
            kb_user=KebeleBusiness.objects.get(id=kb_id)
            kebele_admin_user_obj = kb_user.created_by.user
            resources=Resource.objects.filter(user=kebele_admin_user_obj)
            serializer = ResourceSerializer(resources, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e)
    else:
        return Response("token not provided")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebelebusiness'])
def distributeRecource(request):
    data = request.data
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            kb_id=request_user.kebelebusiness.id
            kb_user=KebeleBusiness.objects.get(id=kb_id)
            kebele_admin_user_obj = kb_user.created_by.user
            resource=Resource.objects.filter(id=data['resource_id'])
            if resource:
                if int(resource.amount) >int(data['amount']):
                    transaction= ResourceTransaction.objects.create(
                        sold_recource=resource.name,
                        amount=data['amount'],
                        buyer=data['buyer'],
                        seller=kb_id,
                        price_perKilo=resource.price_perKilo,
                        supervisor=kebele_admin_user_obj.id
                    )
                    resource.amount=int(resource.amount) - int(data['amount'])
                    resource.save
                    serializer = ResourceTransactionSerializer(transaction, many=False)
                    return Response(serializer.data)
                else:
                    return Response("not enouogh amount")
            else:    
                 return Response("resource not found")
        except Exception as e:
            return Response(e)
    else:
        return Response("token not provided")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['kebeleadmin'])
def getResourceTransactions(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        try:
            request_user , token = response
            transactions = ResourceTransaction.objects.filter(supervisor=request_user.user.id)
            serializer = ResourceTransactionSerializer(transactions, many=True)
            return Response(serializer.data)
        except:
            return Response("something went wrong in the try block") 