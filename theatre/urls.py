from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    ArtistViewSet,
    GenreViewSet,
    PlayViewSet,
    PerformanceViewSet,
)

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("artists", ArtistViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "theatre"
