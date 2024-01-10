from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import mixins

from django.db.models.query import QuerySet
from django.db.models import Count, F

from theatre.models import (
    Artist,
    Genre,
    Play,
    Performance,
)
from theatre.serializers import (
    ArtistSerializer,
    ArtistListSerializer,
    ArtistDetailSerializer,
    GenreSerializer,
    PlaySerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    PerformanceSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    ImageSerializer,
)


class UploadImageMixin:

    upload_image_field = "image"

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request: Request, pk: int = None) -> Response:
        """Endpoint for uploading image to specific object"""
        _object = self.get_object()
        serializer = self.get_serializer(_object, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    GenericViewSet,
    UploadImageMixin
):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_serializer_class(self) -> ArtistSerializer:

        if self.action == "list":
            return ArtistListSerializer

        if self.action == "retrieve":
            return ArtistDetailSerializer

        if self.action == "upload-image":
            return ImageSerializer

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
    GenericViewSet,
):
    queryset = Play.objects.prefetch_related("genres", "artists")
    serializer_class = PlaySerializer

    def get_serializer_class(self) -> PlaySerializer:
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer


class PerformanceViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    UploadImageMixin,
    GenericViewSet
):
    queryset = (
        Performance.objects.all()
        .select_related("play", "theatre_hall")
        .annotate(
            tickets_available=(
                F("theatre_hall__rows") + F("theatre_hall__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = PerformanceSerializer

    def get_serializer_class(self) -> PerformanceSerializer:
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        if self.action == "upload-image":
            return ImageSerializer
        return PerformanceSerializer
