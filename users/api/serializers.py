from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmPassword']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate(self, data):
        password = data.get('password')
        confirm_password =  data.pop('confirmPassword')
        
        if password != confirm_password:
            raise serializers.ValidationError({'error': "Password field didn't match."})
        
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({'error': "Email is already in use."})
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
    # user_count = serializers.IntegerField()
    # users = serializers.String