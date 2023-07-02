from django.urls import path
from .views import index, register, RegistrationView

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('api/clients/create', RegistrationView.as_view())

]
