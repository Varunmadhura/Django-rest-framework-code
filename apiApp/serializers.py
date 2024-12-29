from rest_framework import serializers
from apiApp.models import Register, Login, CommandExecutingLog
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['id','username','email', 'mobile', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterSerializer, self).create(validated_data)

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = "__all__"

class CommandExecutingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandExecutingLog
        fields = ['hostname','username','password','command','output','error','executed_at']
        read_only_fields = ['output', 'error', 'execution_at']


