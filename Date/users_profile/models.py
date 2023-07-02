from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    login = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    avatar = models.ImageField(upload_to='media')
    gender = models.CharField(max_length=25)
    liked = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='date_list')

    # добавляем новое поле, чтобы следить за всеми входящими и исходящими лайками
    def is_like_me(self, user_profile):
        return user_profile.liked.filter(id=self.pk).exists()

    # Это для проверки на совместимость. есть ли данный участник у запрашиваемого
    def __str__(self):
        return f'{self.first_name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
