from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Training, Exercise, TrainingPlan, TrainingResult, Reminder
from .permissions import IsTrainer, IsClient
from .serializers import TrainingSerializer, ExerciseSerializer, TrainingResultSerializer, ReminderSerializer, \
    TrainingPlanSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TrainingFilter


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TrainingFilter

    def get_permissions(self):
        user = self.request.user
        if (
                user and hasattr(user, 'role')
                and user.role in ['client', 'trainer']
                and self.action in ['list', 'retrieve']
        ):
            return [AllowAny()]
        return [IsAdminUser()]


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsTrainer, IsAdminUser]


class TrainingPlanViewSet(viewsets.ModelViewSet):
    queryset = TrainingPlan.objects.all()
    serializer_class = TrainingPlanSerializer
    permission_classes = [IsTrainer, IsClient, IsAdminUser]


class TrainingResultViewSet(viewsets.ModelViewSet):
    queryset = TrainingResult.objects.all()
    serializer_class = TrainingResultSerializer
    permission_classes = [IsTrainer, IsClient, IsAdminUser]


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [IsTrainer, IsClient, IsAdminUser]