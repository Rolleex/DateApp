from django.urls import path
from .views import index, register, RegistrationView,LikeView

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('api/clients/create', RegistrationView.as_view()),
    path('api/clients/<int:id>/match', LikeView.as_view(), name='like'),
]

