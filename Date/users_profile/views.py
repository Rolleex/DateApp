import os.path
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .forms import UserCreateForm, ProfileRegisterForm
from .serializers import UserSerializer, ProfileSerializer
from PIL import Image


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

            ava = profileform.cleaned_data['avatar'].file
            # забираем файл аватара
            new_ava = add_watermark(ava)
            # функция делает свои дела
            Profile.objects.filter(email=user).update(avatar=new_ava)
            # обновляем обьект модели
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
            profile =profile_serializer.save(email=user.email, login=user)
            if 'avatar' in request.FILES:
                ava = request.FILES['avatar']
                new_ava = add_watermark(ava)
                profile.avatar = new_ava
                profile.save()

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def add_watermark(ava):
    water_path = 'media/media/watermark.png'
    new_ava = Image.open(ava)
    watermark = Image.open(water_path)
    position = (new_ava.width - watermark.width, new_ava.height - watermark.height)
    # Чтобы знак всегда был в углу
    new_ava.paste(watermark, position, watermark)
    filename=f'avatar{uuid.uuid4().hex}.png'
    # Присваиваем рандомное имя новой аватарке с водяным знаком
    new_path = os.path.join(settings.MEDIA_ROOT,'')
    save_path = os.path.join(new_path,filename)
    # Кладем аву на место
    new_ava.save(save_path)
    return filename