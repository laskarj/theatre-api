from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


from theatre.models import (
    Genre,
)
from theatre.serializers import (
    GenreSerializer,
)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
