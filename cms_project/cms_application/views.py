from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .get_user import get_user_from_token
from .token_utils import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password,make_password
from .models import User
from .token_utils import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer,PostDeatilsSerializer
from .models import *


class UserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({"success":True,"response":{"user_id":user.user_id},"successmsg": "user created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, *args, **kwargs):
        user = get_user_from_token(request)

        if isinstance(user, Response):
            return user 

        data = request.data.copy()

        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            user = serializer.save()
            return Response({"success":True,"response":{"user_id":user.user_id},"successmsg": "user updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        user = get_user_from_token(request)

        if isinstance(user, Response):
            return user 

        user.delete()
        return Response({"success":True,"response":None,"successmsg": "user deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class UserLoginView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email:
            return Response({"success":False,"response":None,"errormsg": "email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return Response({"success":False,"response":None,"errormsg": "password is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)

            if not check_password(password, user.password):
                return Response({"success":False,"response":None,"errormsg": "invalid password"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"success":False,"response":None,"errormsg": "user with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        token = generate_token(user)

        user.token = token
        user.save()

        return Response({
            "success":True,
            "response":{"token":token},
            "successmsg": "login successfully"
        }, status=status.HTTP_200_OK)



class UserDetailView(APIView):

    def get(self, request, *args, **kwargs):
        user = get_user_from_token(request)

        if isinstance(user, Response):
            return user  

        serializer = UserDetailsSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)




class PostView(APIView):

    def post(self, request, *args, **kwargs):
        user = get_user_from_token(request)

        if isinstance(user, Response):
            return user  

        data = request.data.copy()
        data['post_user'] = user.user_id

        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            post = serializer.save()  
            return Response({"success":True,"response":{"post_id":post.post_id},"successmsg": "post created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def get(self, request, *args, **kwargs):
            user = get_user_from_token(request)

            if isinstance(user, Response):
                return Response({"success":False,"response":None,"errormsg": "authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

            public_posts = Post.objects.filter(is_private=False)

            private_posts = Post.objects.filter(post_user=user, is_private=True)

            all_posts = public_posts | private_posts  

            serializer = PostDeatilsSerializer(all_posts, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
    




class PostDetailView(APIView):

    def get(self, request, id, *args, **kwargs):
        user = get_user_from_token(request)

        if isinstance(user, Response):
            return Response({"success":False,"response":None,"errormsg": "authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(post_id=id)

            if post.is_private and post.post_user != user:
                return Response({"success":False,"response":None,"errormsg": "this is a private post. you are not the owner."}, status=status.HTTP_403_FORBIDDEN)

            serializer = PostDeatilsSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"success":False,"response":None,"errormsg": "post not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request, id, *args, **kwargs):
        user = get_user_from_token(request)

        if isinstance(user, Response):
            return Response({"success":False,"response":None,"errormsg": "authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(post_id=id)
            
            if post.post_user != user:
                return Response({"success":False,"response":None,"errormsg": "you are restricted from updating this post because you are not the owner."}, 
                                status=status.HTTP_403_FORBIDDEN)

        except Post.DoesNotExist:
            return Response({"success":False,"response":None,"errormsg": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostDeatilsSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  
            return Response({"success":True,"response":{"post":serializer.data},"successmsg": "post updated successfully"}, 
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        user = get_user_from_token(request)

        if isinstance(user, Response):
            return Response({"success":False,"response":None,"errormsg": "authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(post_id=id)
            
            if post.post_user != user:
                return Response({"success":False,"response":None,"errormsg": "you are restricted from deleting this post because you are not the owner."}, 
                                status=status.HTTP_403_FORBIDDEN)

            post.delete()  # Delete the post
            return Response({"success":True,"response":None,"successmsg": "post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return Response({"success":False,"response":None,"errormsg": "post not found"}, status=status.HTTP_404_NOT_FOUND)






class LikeView(APIView):

    def post(self, request, blog_id, *args, **kwargs):
        user = get_user_from_token(request)

        if isinstance(user, Response):
            return Response({"success":False,"response":None,"errormsg": "authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(post_id=blog_id)
        except Post.DoesNotExist:
            return Response({"success":False,"response":None,"errormsg": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(post_id=post, user_id=user)

        if not created:
            return Response({"success":False,"response":None,"errormsg": "you already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success":True,"response":None,"successmsg": "post liked successfully"}, status=status.HTTP_201_CREATED)

    def delete(self, request, blog_id, *args, **kwargs):
        user = get_user_from_token(request)

        if isinstance(user, Response):
            return Response({"success":False,"response":None,"errormsg": "authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(post_id=blog_id)
        except Post.DoesNotExist:
            return Response({"success":False,"response":None,"errormsg": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            like = Like.objects.get(post_id=post, user_id=user)
            like.delete()
            return Response({"success":True,"response":None,"successmsg": "post unliked successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"success":False,"response":None,"errormsg": "you haven't liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)
