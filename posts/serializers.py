from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment

# 기본 serializer
class PostBaseSerializer(serializers.Serializer):
    image = serializers.ImageField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    view_count = serializers.IntegerField()
    writer = serializers.IntegerField()
    bad_post = serializers.BooleanField()

# create 추가
    def create(self, validated_data):
        post = Post.objects.create(
            content = validated_data['content'],
            view_count = validated_data['view_count'],
            # writer = validated_data['writer'],
            writer = validated_data['username'],
        )
        return post
        # return Post.objects.create(validated_data)

# ModelSerializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'       