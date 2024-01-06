from rest_framework import serializers

from theatre.models import (
    Artist,
    Genre,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", )


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("id", "first_name", "last_name", "full_name", )
