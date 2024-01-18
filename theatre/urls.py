from django.urls import include, path
from rest_framework import routers

from theatre.views import (
    ArtistViewSet,
    GenreViewSet,
    PerformanceViewSet,
    PlayViewSet,
    ReservationViewSet,
)

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("artists", ArtistViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = router.urls

app_name = "theatre"
