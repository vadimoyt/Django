from rest_framework.routers import DefaultRouter

from .views import TrainerView


router = DefaultRouter()
router.register(r'trainers', TrainerView, basename='trainer')

urlpatterns = [
    *router.urls,
]