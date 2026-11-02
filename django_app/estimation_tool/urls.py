from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import EstimationCreationView, PlatformListViewSet

router = DefaultRouter()
router.register(r"platforms", PlatformListViewSet, basename="platform")
urlpatterns = router.urls + [
    path("create/", EstimationCreationView.as_view(), name="estimation-list"),
]
