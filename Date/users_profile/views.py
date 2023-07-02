from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .models import Profile
from .forms import UserCreateForm, ProfileRegisterForm


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
