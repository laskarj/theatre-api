from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from django.db.models.query import QuerySet

from theatre.models import (
    Artist,
    Genre,
    Play
)
from theatre.serializers import (
    ArtistSerializer,
    ArtistDetailSerializer,
    GenreSerializer,
    PlaySerializer,
    PlayListSerializer,
    PlayDetailSerializer,
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

    def get_serializer_class(self) -> ArtistSerializer:
        if self.action == "retrieve":
            return ArtistDetailSerializer
        return ArtistSerializer


    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        if self.action == "retrieve":
            queryset = queryset.prefetch_related("plays")

        return queryset


class PlayViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Play.objects.prefetch_related("genres", "artists")
    serializer_class = PlaySerializer

    def get_serializer_class(self) -> PlaySerializer:
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer
