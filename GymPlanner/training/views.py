from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Training
from .serializers import TrainingSerializer


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

    def get_permissions(self):
        user = self.request.user
        if user and hasattr(user, 'role') and user.role == 'client' and self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]