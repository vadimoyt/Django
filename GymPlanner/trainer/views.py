from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import Trainer
from .serializers import TrainerSerializer


class TrainerView(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
