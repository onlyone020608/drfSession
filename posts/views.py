# posts > views.py
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

from .models import Post
from .serializers import *

class PostAPIView(APIView):
    def post(self, request):
        serializer = PostBaseSerializer(data = request.data)
        if serializer.is_valid():
            if serializer.validated_data['bad_post'] == True:
                return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"message": "post success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# PostAPIView2 최종 수정본
class PostAPIView2(APIView):
    def post(self, request):
        serializer = PostSerializer(data = request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            print(serializer.validated_data)
            if serializer.initial_data['bad_post'] == True:
                return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                print(serializer.data)
                return Response({"message": "post success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def PostAPI_FBV(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.initial_data['bad_post'] == True:
            return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response({"message": "post success"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Mixins
# posts > views.py
class PostListCreateMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.initial_data['bad_post'] == True:
            return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request)
    
# GenericView
# posts > views.py
class PostListCreateGeneric(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.initial_data['bad_post'] == True:
            return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request)
    
# ModelViewSet
# posts > views.py
class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentCreateView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            post = get_object_or_404(Post, id=request.data['post'])
            writer = get_object_or_404(User, id=request.data['writer'])
            comment = Comment.objects.create(
                content=request.data['content'],
                post=post,
                writer=writer
            )
            response_serializer = CommentSerializer(comment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)