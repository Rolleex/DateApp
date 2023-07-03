import os.path
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from geopy.distance import great_circle
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .forms import UserCreateForm, ProfileRegisterForm
from .serializers import UserSerializer, ProfileSerializer, ProfileListSerializer
from PIL import Image
from .filters import ProfileFilter
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class Index(View):
    def get(self, request):
        profile_filter = ProfileFilter(request.GET, queryset=Profile.objects.all())
        distance = request.GET.get('distance')
        if distance:
            user_profile = request.user.profile
            filtered_profiles = []
            for profile in profile_filter.qs:
                # перебираем профили
                profile_coordinates = (profile.latitude, profile.longitude)
                user_coordinates = (user_profile.latitude, user_profile.longitude)
                # получаем кординаты
                profile_distance = great_circle(profile_coordinates, user_coordinates).kilometers
                # Получаем дистанцию в км.через great_circle
                if profile_distance <= float(distance):
                    filtered_profiles.append(profile)
                    # добавляем профили для выдачи на главную
            filtered_profile_ids = [profile.id for profile in filtered_profiles]
            # Собираем id профилей
            filtered_queryset = Profile.objects.filter(id__in=filtered_profile_ids)
            # получаем профили с нужными id
            profile_filter = ProfileFilter(request.GET, queryset=filtered_queryset)
            # отображаем все доступные профили из quryset, которые подходят под условия фильтров
        return render(request, 'users_profile/index.html',
                      {'filters': profile_filter})

    def post(self, request):
        profile_id = request.POST.get('profile_id')
        profile = get_object_or_404(Profile, id=profile_id)
        request.user.profile.liked.add(profile)

        if profile.is_like_me(request.user.profile) and request.user.profile.is_like_me(profile):
            # проверка на взаимность
            mail_send(request.user.profile, profile)
            return redirect('home')
        else:
            return redirect('home')


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
            profile = profile_serializer.save(email=user.email, login=user)
            if 'avatar' in request.FILES:
                ava = request.FILES['avatar']
                new_ava = add_watermark(ava)
                profile.avatar = new_ava
                profile.save()

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileListAPIView(APIView):
    serializer_class = ProfileListSerializer
    filterset_class = ProfileFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Profile.objects.all()
        distance = self.request.GET.get('distance')
        if distance:
            user_profile = self.request.user.profile
            filtered_profiles = []
            for profile in queryset:
                # перебираем профили
                profile_coordinates = (profile.latitude, profile.longitude)
                user_coordinates = (user_profile.latitude, user_profile.longitude)
                # получаем координаты
                profile_distance = great_circle(profile_coordinates, user_coordinates).kilometers
                # Получаем дистанцию в км через great_circle
                if profile_distance <= float(distance):
                    filtered_profiles.append(profile)
                    # добавляем профили для выдачи на главную
            filtered_profile_ids = [profile.id for profile in filtered_profiles]
            # Собираем id профилей
            queryset = Profile.objects.filter(id__in=filtered_profile_ids)
            # получаем профили с нужными id
            # дублировали код, но все работает
        return queryset

    def get(self, request, format=None):
        queryset = self.get_queryset()
        filter_backend = DjangoFilterBackend()
        filtered_queryset = filter_backend.filter_queryset(request, queryset, self)
        serializer = self.serializer_class(filtered_queryset, many=True)
        return Response(serializer.data)


class LikeView(APIView):
    def post(self, request, id):
        profile = Profile.objects.get(id=id)
        request.user.profile.liked.add(profile)
        if profile.is_like_me(request.user.profile) and request.user.profile.is_like_me(profile):
            mail_send(request.user.profile, profile)
            return Response({"message": "Ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No mutual like."}, status=status.HTTP_400_BAD_REQUEST)


def add_watermark(ava):
    water_path = 'media/media/watermark.png'
    new_ava = Image.open(ava)
    watermark = Image.open(water_path)
    position = (new_ava.width - watermark.width, new_ava.height - watermark.height)
    # Чтобы знак всегда был в углу
    new_ava.paste(watermark, position, watermark)
    filename = f'avatar{uuid.uuid4().hex}.png'
    # Присваиваем рандомное имя новой аватарке с водяным знаком
    new_path = os.path.join(settings.MEDIA_ROOT, '')
    save_path = os.path.join(new_path, filename)
    # Кладем аву на место
    new_ava.save(save_path)
    return filename


def mail_send(me, you):
    send_mail(
        f"Вы понравились {me}!",
        f"Вы понравились {me}!Почта участника:{me.email}",
        me.email,
        [you.email],
        fail_silently=False,
    )
    send_mail(
        f"Вы понравились {you}!",
        f"Вы понравились {you}! Почта участника:{you.email}",
        you.email,
        [me.email],
        fail_silently=False,

    )
