import django_filters
from training.models import Training

class TrainingFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains', label='title'
    )
    type = django_filters.ChoiceFilter(choices=Training.CHOICE_TYPE, label='type')
    level = django_filters.ChoiceFilter(choices=Training.CHOICE_LEVEL, label='level')

    class Meta:
        model = Training
        fields = ['title', 'type', 'level']
