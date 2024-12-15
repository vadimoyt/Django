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
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            if hasattr(user, 'role') and user.role == 'trainer':
                return [IsTrainer()]
        return [IsAdminUser()]


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser(), IsTrainer()]


class TrainingPlanViewSet(viewsets.ModelViewSet):
    queryset = TrainingPlan.objects.all()
    serializer_class = TrainingPlanSerializer

    def get_permissions(self):
        user = self.request.user
        if self.action in ['list', 'retrieve']:
            return [IsTrainer() | IsAdminUser() | IsClient()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            if hasattr(user, 'role') and user.role == 'trainer':
                return [IsTrainer()]
        return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role in ['client', 'trainer']:
            return self.queryset.filter(user=user)
        return self.queryset


class TrainingResultViewSet(viewsets.ModelViewSet):
    queryset = TrainingResult.objects.all()
    serializer_class = TrainingResultSerializer

    def get_permissions(self):
        user = self.request.user
        if self.action in ['list', 'retrieve']:
            return [IsTrainer(), IsAdminUser(), IsClient()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            if hasattr(user, 'role') and user.role == 'trainer':
                return [IsTrainer()]
        return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role in ['client', 'trainer']:
            return self.queryset.filter(user=user)
        return self.queryset



class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer

    def get_permissions(self):
        user = self.request.user
        if self.action in ['list', 'retrieve']:
            return [IsTrainer(), IsAdminUser(), IsClient()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            if hasattr(user, 'role') and user.role == 'trainer':
                return [IsTrainer()]
        return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role in ['client', 'trainer']:
            return self.queryset.filter(user=user)
        return self.queryset