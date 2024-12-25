from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from GymPlanner.permissions import IsClient, IsOwnerOrAdmin
from .filters import TrainerFilters
from .models import Trainer, RatingOfTrainer
from .serializers import TrainerSerializer, RatingSerializer


class TrainerView(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TrainerFilters


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class RatingOfTrainerView(viewsets. ModelViewSet):
    queryset = RatingOfTrainer.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        user = self.request.user
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create']:
            return [IsClient()]
        elif self.action in [ 'update', 'destroy', 'partial_update']:
            return [IsOwnerOrAdmin()]
        return [IsAdminUser()]

