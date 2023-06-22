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
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebele_admin'])
def getResources(request):
    response = JWT_authenticator.authenticate(request)
    request_user , token = response
    resources = Resource.objects.filter(user=request_user)
    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal'])
def createResource(request):
    data = request.data
    print(data)
    response = JWT_authenticator.authenticate(request)
    request_user , token = response
    user=User.objects.get(id=request_user.id)
    try:
        if(user):
            resource = Resource.objects.create(
                name=data['name'],
                type=data['type'],
                amount=data['amount'],
                price_perKilo=data['price_perKilo'],
                user=user
            )       
            serializer = ResourceSerializer(resource, many=False)
            return Response(serializer.data)
        else:
            return Response("user not found")
    except:
        return Response("something went wrong in the try block") 
        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebele_admin'])
def getResource(request, pk):
    try:
        resource = Resource.objects.get(id=pk)
        serializer = ResourceSerializer(resource, many=False)
        return Response(serializer.data)
    except:
        return Response("resource not found!!!")


@api_view(['PUT'])
def updateResource(request, pk):
    data = request.data
    resource = Resource.objects.get(id=pk)
    serializer = ResourceSerializer(instance=resource, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors) 
    
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebele_admin'])
def transferResource(request):
    try:
        data = request.data
        response = JWT_authenticator.authenticate(request)
        request_user , token = response
        user=User.objects.get(id=request_user.id)
        resource=request_user.resource_set.get(id=data['resource_id'])
        if resource and user:
            newresource = SentResource.objects.create(
                name=resource.name,
                type=resource.type,
                status="pending",
                amount=data['amount'],
                price_perKilo=resource.price_perKilo,
                sender=user,
                reciever=data['to'],
            )   
            newrecource=SentResource.objects.get(id=newresource.id)
            serializer = SentResourceSerializer(newrecource, many=False)
            return Response(serializer.data)
        else:
            return Response("no mathing resource or user found")
    except Exception:
        return Response(Exception)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebele_admin'])
def getSentResource(request):
    try:
        response = JWT_authenticator.authenticate(request)
        request_user , token = response
        resources=SentResource.objects.filter(sender=request_user.id)
        serializer = SentResourceSerializer(resources, many=True)
        return Response(serializer.data)
        
    except Exception:
        return Response(Exception)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebele_admin'])
def getrecievedResource(request):
    try:
        response = JWT_authenticator.authenticate(request)
        request_user , token = response
        resources=SentResource.objects.filter(reciever=request_user.id)
        serializer = SentResourceSerializer(resources, many=True)
        return Response(serializer.data)
        
    except Exception:
        return Response(Exception)
    




# deal with this later
@api_view(['POST'])
def acceptResource(request):
    try:
        data = request.data
        resource = Resource.objects.get(id=data['resource_id'])
        to=User.objects.get(id=data['to'])
        resource_old=Resource.objects.get(user=to , name=resource.name)
        
        if resource_old:
            print("user have it already have this resource so only update the amount")
            resource_old.amount=data['amount']
            resource_old.save()
            # serializer = ResourceSerializer(resource_old, many=False)
            return Response("done")
        else:
            print("user dont have this resource tpe so create new field for him")
            newresource = Resource.objects.create(
            name=resource.name,
            type=resource.type,
            amount=data['amount'],
            price_perKilo=resource.price_perKilo,
            user=to,
        )       
            

        serializer = ResourceSerializer(resource_old, many=True)
        return Response(serializer.data)
    except Exception:
        return Response(Exception)

