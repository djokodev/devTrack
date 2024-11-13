from rest_framework import serializers
from .models import User
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared')

    def validate_date_of_birth(self, value):
        if value:
            today = date.today()
            age_in_days = (today - value).days
            age = age_in_days // 365
            if age < 16:
                raise serializers.ValidationError("You must be at least 16 years old to register.")
        return value
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password or confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")

        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user