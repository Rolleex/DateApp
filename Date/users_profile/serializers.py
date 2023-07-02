from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Емейл')
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password1']
        user = User.objects.create_user(username=email, password=password, email=email)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=(('Мужчина', 'male'), ('Женщина', 'female')))

    class Meta:
        model = Profile
        exclude = ('email', 'login')
