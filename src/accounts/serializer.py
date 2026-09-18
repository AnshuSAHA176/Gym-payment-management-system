from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,    
                      
            },
            'email': {
                'required': True,     
                'allow_blank': False  
            }
        }

    def create(self, validated_data):
        user = User.objects.create_superuser(
            **validated_data
        )
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):

        user = authenticate(email=attrs['email'],password=attrs['password'])

        if  user == None:
            raise serializers.ValidationError("wrong email and password")

        attrs['user'] = user

        return attrs
    
