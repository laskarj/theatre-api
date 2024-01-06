from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    ArtistViewSet,
    GenreViewSet,
)

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("artists", ArtistViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "theatre"
