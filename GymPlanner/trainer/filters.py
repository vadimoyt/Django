import django_filters

from trainer.models import Trainer


class TrainerFilters(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        field_name='first_name', lookup_expr='icontains', label='first name'
    )
    last_name = django_filters.CharFilter(
        field_name='last_name', lookup_expr='icontains', label='surname'
    )

    class Meta:
        model = Trainer
        fields = ['first_name', 'last_name']