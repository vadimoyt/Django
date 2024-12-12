from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from django.views.decorators.cache import cache_page
from .models import Trainer
from .serializers import TrainerSerializer


class TrainerView(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

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
