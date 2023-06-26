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
def getPosts(request):
        try:
            posts = Post.objects.all().order_by('-created_at')
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e) 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    data = request.data
    response = JWT_authenticator.authenticate(request)
    request_user , token = response
    user=User.objects.get(id=request_user.id)
    try:
        if user:
            post = Post.objects.create(
                posted_by=user,
                title = request.POST.get('title'),
                discription = request.POST.get('discription'),
                thumbnail = request.FILES.get('thumbnail'),
                rank = "0"
            )  
            print("dershalew\n")     
            _post=Post.objects.get(id=post.id)
            serializer = PostSerializer(_post, many=False)
            return Response(serializer.data)
        else:
            return Response("user not found")
    except Exception as e:
        return Response(e) 

@api_view(['DELETE'])
def deletePost(request, pk):
    try:
        post = Post.objects.get(id=pk)
        post.delete()
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(e) 
    
   