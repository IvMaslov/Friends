from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(request=self.context.get("request"), username=username, password=password)
            if not user:
                raise serializers.ValidationError("Wrong authorization creadentioals", "authorization")
        else:
            raise serializers.ValidationError("Require username and password", "authorization")
        attrs["user"] = user
        return attrs
    

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return attrs
            else:
                raise serializers.ValidationError("User already exists", "authorization")
        else:
            raise serializers.ValidationError("Require username and password", "authorization")
        
    def create(self, validated_data):
        User.objects.create_user(username=validated_data["username"], password=validated_data["password"])
