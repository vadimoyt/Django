from rest_framework.routers import DefaultRouter

from .views import TrainerView, RatingOfTrainerView

router = DefaultRouter()
router.register(r'trainers', TrainerView, basename='trainer')
router.register(r'rait_list', RatingOfTrainerView, basename='rait-list')

urlpatterns = [
    *router.urls,
]