from rest_framework.routers import DefaultRouter

from .views import TrainingViewSet

router = DefaultRouter()
router.register(r'trainings', TrainingViewSet, basename='trainings')

urlpatterns = [
    *router.urls,
]