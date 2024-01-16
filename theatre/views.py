from datetime import datetime

from django.db.models import Count, F, Q
from django.db.models.query import QuerySet
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated

from theatre.models import Artist, Genre, Performance, Play, Reservation

from theatre.permissions import IsAdminUserOrReadOnly
from theatre.serializers import (
    ArtistDetailSerializer,
    ArtistListSerializer,
    ArtistSerializer,
    GenreSerializer,
    ImageSerializer,
    PerformanceDetailSerializer,
    PerformanceListSerializer,
    PerformanceSerializer,
    PlayDetailSerializer,
    PlayListSerializer,
    PlaySerializer,
    ReservationListSerializer,
    ReservationSerializer,
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


class PaginationMixin:
    """
    Mixin class for providing custom pagination configuration.
    Attributes:
        None

    Methods:
        Create and configure a PageNumberPagination instance:
            get_pagination(
            page_size: int,
             max_pages: int
             ) -> PageNumberPagination:

    Usage:
        Inherit from this mixin in a
        Django REST Framework ViewSet
        to customize pagination settings.
    """

    def get_pagination(
            self,
            page_size: int,
            max_pages: int
    ) -> PageNumberPagination:
        """
        Create and configure a PageNumberPagination
        instance with custom settings.

        Args:
            page_size (int): The number of items per page.
            max_pages (int): The maximum number of pages allowed.

        Returns:
            PageNumberPagination: Configured instance of PageNumberPagination.
        """
        paginator = PageNumberPagination
        paginator.page_size, paginator.max_page_size = page_size, max_pages

        return paginator


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class ArtistViewSet(
    UploadImageMixin,
    PaginationMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pagination_class = self.get_pagination(10, 100)

    def get_serializer_class(self) -> Serializer:
        if self.action == "list":
            return ArtistListSerializer

        if self.action == "retrieve":
            return ArtistDetailSerializer

        if self.action == "upload-image":
            return ImageSerializer

        return ArtistSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("plays")

        return queryset


class PlayViewSet(
    PaginationMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Play.objects.prefetch_related("genres", "artists")
    serializer_class = PlaySerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pagination_class = self.get_pagination(10, 100)

    @staticmethod
    def _params_to_ints(query: str) -> list[int]:
        """Convert query string ids to a list of integer ids."""
        return [int(str_id) for str_id in query.split(",")]

    def get_queryset(self) -> QuerySet:
        """Retrieve the queryset with filters"""
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        artists = self.request.query_params.get("artists")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            genres_ids = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genres_ids)

        if artists:
            artists_ids = self._params_to_ints(artists)
            queryset = queryset.filter(artists__id__in=artists_ids)

        return queryset.distinct()

    def get_serializer_class(self) -> Serializer:
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer


class PerformanceViewSet(
    UploadImageMixin,
    PaginationMixin,
    ModelViewSet,
):
    queryset = (
        Performance.objects.all()
        .select_related("play", "theatre_hall")
        .annotate(
            tickets_available=(
                F("theatre_hall__rows")
                + F("theatre_hall__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = PerformanceSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pagination_class = self.get_pagination(10, 100)

    def get_serializer_class(self) -> Serializer:
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        if self.action == "upload-image":
            return ImageSerializer
        return PerformanceSerializer

    def get_queryset(self) -> QuerySet:
        date = self.request.query_params.get("date")
        play_id_str = self.request.query_params.get("play")

        queryset = self.queryset

        if play_id_str:
            queryset = queryset.filter(play_id=int(play_id_str))

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        return queryset


class ReservationViewSet(
    PaginationMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.prefetch_related(
        "tickets__performance__play", "tickets__performance__theatre_hall"
    )
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pagination_class = self.get_pagination(10, 100)

    def get_queryset(self) -> QuerySet:
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self) -> ReservationSerializer:
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user=self.request.user)
