from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from django.views.decorators.cache import cache_page

from GymPlanner.permissions import IsTrainer, IsClient, IsOwnerOrAdmin
from .models import Trainer, RatingOfTrainer
from .serializers import TrainerSerializer, RatingSerializer
from .filters import TrainerFilters
from django_filters.rest_framework import DjangoFilterBackend


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

