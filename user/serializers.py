from rest_framework import serializers
from .models import User
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared')

    def validate_date_of_birth(self, value):
        if value:
            today = date.today()
            age = today.year - value.year
            if today.month < value.month or (today.month == value.month and today.day < value.day):
                age -= 1
            if age < 16:
                raise serializers.ValidationError("You must be at least 16 years old to register.")
        return value

    def create(self, validated_data):
        can_be_contacted = validated_data.pop('can_be_contacted', True)
        can_data_be_shared = validated_data.pop('can_data_be_shared', True)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data['date_of_birth'],
            can_be_contacted=can_be_contacted,
            can_data_be_shared=can_data_be_shared
        )
        return user