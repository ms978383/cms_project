from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'name', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
    

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'user_id','name', 'email', 'password','token']




class PostSerializer(serializers.ModelSerializer):
    is_private = serializers.BooleanField(required=True)  # Set is_private as required

    class Meta:
        model = Post
        fields = ['post_user', 'title', 'description', 'content','is_private']



class PostDeatilsSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['post_id', 'post_user', 'title', 'description', 'content', 'creation_date', 'is_private', 'likes']

    def get_likes(self, obj):
        likes = Like.objects.filter(post_id=obj)
        return [{'like_id': like.like_id, 'user_id': like.user_id.user_id} for like in likes]



        


