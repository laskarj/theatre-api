from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


from theatre.models import (
    Artist,
    Genre,
)
from theatre.serializers import (
    ArtistSerializer,
    GenreSerializer,
)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ArtistViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
