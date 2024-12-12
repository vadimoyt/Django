from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Training
from .serializers import TrainingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TrainingFilter


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TrainingFilter

    def get_permissions(self):
        user = self.request.user
        if user and hasattr(user, 'role') and user.role == 'client' and self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]