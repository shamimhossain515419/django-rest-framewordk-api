from rest_framework import serializers
from .models import Person , Color

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']

class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
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
