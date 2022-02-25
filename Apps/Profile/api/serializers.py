from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Profile



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions', 'last_login']
        read_only_fields = ['date_joined', 'email', 'is_active', 'is_staff', 'is_superuser', 'username']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'avatar']
    
    def update(self, instance: Profile, validated_data):
        User.objects.filter(pk=instance.user.pk).update(**validated_data.pop('user', {}))
        return super().update(instance, validated_data)


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=1, max_length=100, required=True)
