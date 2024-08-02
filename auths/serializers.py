from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import serializers
import re

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        ref_name = "userSerializer"
        model = CustomUser
        # Add more fields as needed
        fields = ('id', 'email', 'password', 'confirm_password')
        # Password should not be read
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        if len(value) < 6: 
            raise serializers.ValidationError(
                "Password must be at least 6 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9!@#$%^&*()_+=-]', value):
            raise serializers.ValidationError(
                "Password must contain at least one number or symbol.")
        return value

    # def validate_email(self, value):
    #     if User.objects.filter(email=value).exists():
    #         raise ValidationError("An account with that Email already exists!")
    #     return value
    
    def save(self):
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        
        if password != confirm_password:
            raise ValidationError({'Error':'Password should be the same as confirm pasword'})
        
        if CustomUser.objects.filter(email=self.validated_data['email']).exists():
            raise ValidationError({'Error':"Email already exists!"})
        
        account = CustomUser(email=self.validated_data['email'])
        account.set_password(password)
        account.save()
        return account


        

        
        
        
