from django.urls import path
from .views import Index, register, RegistrationView, LikeView, ProfileListAPIView

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('register/', register, name='register'),
    path('api/clients/create', RegistrationView.as_view()),
    path('api/clients/<int:id>/match', LikeView.as_view(), name='like'),
    path('api/list', ProfileListAPIView.as_view())
]
