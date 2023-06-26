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
    response = JWT_authenticator.authenticate(request)
    request_user , token = response
    user=User.objects.get(id=request_user.id)
    try:
        if user:
            resource = Resource.objects.create(
                name=data['name'],
                type=data['type'],
                amount=data['amount'],
                price_perKilo=data['price_perKilo'],
                user=user
            )  
            print("dershalew\n")     
            _resource=Resource.objects.get(id=resource.id)
            serializer = ResourceSerializer(_resource, many=False)
            return Response(serializer.data)
        else:
            return Response("user not found")
    except Exception as e:
        return Response(e) 
        


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
        if int(resource.amount) < int(data['amount']):
            return Response("no enough resource left")
        if resource and user:
            resource.amount=int(resource.amount)-int(data['amount'])
            resource.save()
            newresource = SentResource.objects.create(
                name=resource.name,
                type=resource.type,
                status="pending",
                amount=data['amount'],
                price_perKilo=resource.price_perKilo,
                sender=user,
                reciever=data['to'],
            )   
            _newrecource=SentResource.objects.get(id=newresource.id)
            serializer = SentResourceSerializer(_newrecource, many=False)
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
        user=User.objects.get(id=request_user.id)
        resources=SentResource.objects.filter(sender=user).order_by('created_at')
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
        user=User.objects.get(id=request_user.id)
        resources=SentResource.objects.filter(reciever=user.id)
        serializer = SentResourceSerializer(resources, many=True)
        return Response(serializer.data)
        
    except Exception:
        return Response(Exception)
    





@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebele_admin'])
def acceptResource(request):
    try:
        data = request.data
        print(data)

        response = JWT_authenticator.authenticate(request)
        request_user , token = response
        user=User.objects.get(id=request_user.id)
        print(data)
        sentresource = SentResource.objects.filter(id=data['resource_id']).first()
        resource_old=Resource.objects.filter(user=user , name=sentresource.name).first()

        if resource_old:
            print("user have it already have this resource so only update the amount")
            resource_old.amount=int(resource_old.amount)+int(sentresource.amount)
            resource_old.save()
            print("uih delete from sent recource")
            sentresource.delete()
            rec=SentResource.objects.filter(reciever=user.id)
            serializer = SentResourceSerializer(rec, many=True)
            return Response(serializer.data)
        else:
            print("user dont have this resource tpe so create new field for him")
            print(sentresource.name,sentresource.type,sentresource.price_perKilo,sentresource.amount,)
            newresource = Resource.objects.create(
            name=sentresource.name,
            type=sentresource.type,
            amount=sentresource.amount,
            price_perKilo=sentresource.price_perKilo,
            user=user,
        )    
            print(newresource)
            print("uih delete from sent recource")
            sentresource.delete()
            rec=SentResource.objects.filter(reciever=user.id)
            serializer = SentResourceSerializer(rec, many=True)
            return Response(serializer.data)
    except Exception:
        return Response(Exception)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebele_admin'])
def declineResource(request):
    try:
        data = request.data
        response = JWT_authenticator.authenticate(request)
        request_user , token = response
        user=User.objects.get(id=request_user.id)
        sentresource = SentResource.objects.filter(id=data['resource_id']).first()
        print("rreached here",sentresource.sender,"\n\n")

        sender=User.objects.get(username=sentresource.sender)
        resource_old=Resource.objects.filter(user=sender , name=sentresource.name).first()
        print("reached here")
        if resource_old:
            print("user have it already have this resource so only update the amount")
            resource_old.amount=int(resource_old.amount)+int(sentresource.amount)
            resource_old.save()
            print("uih delete from sent recource")
            sentresource.delete()
            rec=SentResource.objects.filter(reciever=user.id)
            serializer = SentResourceSerializer(rec, many=True)
            return Response(serializer.data)
        else:
            print("user dont have this resource tpe so create new field for him")
            newresource = Resource.objects.create(
            name=sentresource.name,
            type=sentresource.type,
            amount=sentresource.amount,
            price_perKilo=sentresource.price_perKilo,
            user=sender,
        )    
            print(newresource)
            print("uih delete from sent recource")
            sentresource.delete()
            rec=SentResource.objects.filter(reciever=user.id)
            serializer = SentResourceSerializer(rec, many=True)
            return Response(serializer.data)
    except Exception as e:
        print (e)
        return Response(e)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebele_admin'])
def acceptResource(request):
    try:
        data = request.data
        print(data)

        response = JWT_authenticator.authenticate(request)
        request_user , token = response
        user=User.objects.get(id=request_user.id)
        print(data)
        sentresource = SentResource.objects.filter(id=data['resource_id']).first()
        resource_old=Resource.objects.filter(user=user , name=sentresource.name).first()

        if resource_old:
            print("user have it already have this resource so only update the amount")
            resource_old.amount=int(resource_old.amount)+int(sentresource.amount)
            resource_old.save()
            print("uih delete from sent recource")
            sentresource.delete()
            rec=SentResource.objects.filter(reciever=user.id)
            serializer = SentResourceSerializer(rec, many=True)
            return Response(serializer.data)
        else:
            print("user dont have this resource tpe so create new field for him")
            print(sentresource.name,sentresource.type,sentresource.price_perKilo,sentresource.amount,)
            newresource = Resource.objects.create(
            name=sentresource.name,
            type=sentresource.type,
            amount=sentresource.amount,
            price_perKilo=sentresource.price_perKilo,
            user=user,
        )    
            print(newresource)
            print("uih delete from sent recource")
            sentresource.delete()
            rec=SentResource.objects.filter(reciever=user.id)
            serializer = SentResourceSerializer(rec, many=True)
            return Response(serializer.data)
    except Exception:
        return Response(Exception)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_rolls=['federal','region','zone','woreda','kebele_admin'])
def cancelResource(request):
    try:
        data = request.data
        response = JWT_authenticator.authenticate(request)
        request_user , token = response
        user=User.objects.get(id=request_user.id)
        sentresource = SentResource.objects.filter(id=data['resource_id']).first()
        print("rreached here",sentresource.sender,"\n\n")

        sender=User.objects.get(username=sentresource.sender)
        resource_old=Resource.objects.filter(user=sender , name=sentresource.name).first()
        print("reached here")
        if resource_old:
            print("user have it already have this resource so only update the amount")
            resource_old.amount=int(resource_old.amount)+int(sentresource.amount)
            resource_old.save()
            print("uih delete from sent recource")
            sentresource.delete()
            rec=SentResource.objects.filter(sender=user.username)
            serializer = SentResourceSerializer(rec, many=True)
            return Response(serializer.data)
        else:
            print("user dont have this resource tpe so create new field for him")
            newresource = Resource.objects.create(
            name=sentresource.name,
            type=sentresource.type,
            amount=sentresource.amount,
            price_perKilo=sentresource.price_perKilo,
            user=sender,
        )    
            print(newresource)
            print("uih delete from sent recource")
            sentresource.delete()
            rec=SentResource.objects.filter(sender=user.username)
            serializer = SentResourceSerializer(rec, many=True)
            return Response(serializer.data)
    except Exception as e:
        print (e)
        return Response(e)