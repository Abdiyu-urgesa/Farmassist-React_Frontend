from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from ..serializers import *
from ..models import *

@api_view(['GET'])
def getdiseases(request):
    diseases = Disease.objects.all()
    serializer = DiseaseSerializer(diseases, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createDisease(request):
    data = request.data
    try:
        disease = Disease.objects.create(
            name=data['name'],
            crop=data['crop'],
            user=User.objects.get(id= data['user'])
        )       
        serializer = DiseaseSerializer(disease, many=False)
        return Response(serializer.data)
    
    except:
        return Response("something went wrong in the try block") 
        


@api_view(['GET'])
def getDisease(request, pk):
    try:
        disease = Disease.objects.get(id=pk)
        serializer = DiseaseSerializer(disease, many=False)
        return Response(serializer.data)
    except:
        return Response("user not found")


@api_view(['PUT'])
def updateFarmer(request, pk):
    data = request.data
    disease = Disease.objects.get(id=pk)
    serializer = DiseaseSerializer(instance=disease, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    
    return Response(serializer.data)

