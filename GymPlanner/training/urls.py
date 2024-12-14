from rest_framework.routers import DefaultRouter

from .views import TrainingViewSet, ExerciseViewSet, TrainingPlanViewSet, TrainingResultViewSet, ReminderViewSet

router = DefaultRouter()
router.register(r'trainings', TrainingViewSet, basename='trainings')
router.register(r'exercises', ExerciseViewSet, basename='exercises')
router.register(r'training_plan', TrainingPlanViewSet, basename='training_plan')
router.register(r'training_result', TrainingResultViewSet, basename='training_result')
router.register(r'reminder', ReminderViewSet, basename='reminder')

urlpatterns = [
    *router.urls,
]