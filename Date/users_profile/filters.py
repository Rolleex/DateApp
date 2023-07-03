import django_filters
from django_filters import FilterSet

from .models import Profile


class ProfileFilter(FilterSet):
    GENDER_CHOICES = [('', 'All'),
                      ('Мужчина', 'Male'),
                      ('Женщина', 'Female'), ]
    gender = django_filters.ChoiceFilter(choices=GENDER_CHOICES, field_name='gender')
    first_name = django_filters.CharFilter(lookup_expr='icontains', field_name='first_name')
    last_name = django_filters.CharFilter(lookup_expr='icontains', field_name='last_name')

    class Meta:
        model = Profile
        fields = ['gender', 'first_name', 'last_name']

