from rest_framework import serializers
from .models import Person , Color
from django.contrib.auth.models import User

class loginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class PeopleSerializer(serializers.ModelSerializer):
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all())
    class Meta:
        model = Person
        fields = '__all__'
        # depth = 1    

    def validate(self, data):
        if data['age'] < 18:  # Ensuring age is at least 18
            raise serializers.ValidationError({'age': 'Age should be at least 18'})

        if len(data['name']) > 20:  # Limiting name length to 20 characters
            raise serializers.ValidationError({'name': 'Name should not exceed 20 characters'})

        return data




class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
         if data['username']:
             if User.objects.filter(username=data['username']).exists():
                 raise serializers.ValidationError({'username': 'Username already exists'})
         if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError({'email': 'email already exists'})      
         return data    

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data 
             

