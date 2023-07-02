from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .forms import UserCreateForm, ProfileRegisterForm
from .serializers import UserSerializer, ProfileSerializer


# Create your views here.


def index(request):
    profile = Profile.objects.all()
    return render(request, 'users_profile/index.html', {'profiles': profile})


def register(request):
    if request.method == 'POST':
        userform = UserCreateForm(request.POST)
        profileform = ProfileRegisterForm(request.POST, request.FILES)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save(commit=False)
            user.username = user.email
            user.save()

            profile = profileform.save(commit=False)
            profile.login = user
            profile.email = user
            profile.save()
            auth_user = authenticate(request, username=user.email, password=request.POST['password1'])
            if auth_user is not None:
                login(request, auth_user)

            return redirect('home')
    else:

        userform = UserCreateForm()
        profileform = ProfileRegisterForm()

    return render(request, 'users_profile/register.html', {'userform': userform, 'profileform': profileform})


class RegistrationView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        profile_serializer = ProfileSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True) and profile_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            profile_serializer.save(email=user, login=user)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
