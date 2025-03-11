
from rest_framework.serializers import ModelSerializer, Serializer
from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate


class CustomUserSerializer(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields =("id", "email", "username")

class RegisterUserSerializer(ModelSerializer): 
    class Meta:
        model = CustomUser 
        fields = ('email', 'password','username')
        extra_kwargs = {'password': {'write_only': True}} 


    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user    

class LoginUserSerializer(Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials!")


from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source="author.email", read_only=True)
    class Meta:
        model = Blog
        fields = ["id", "author", "author_email", "title", "content", "created_at", "updated_at"]
        read_only_fields = ["author"]



