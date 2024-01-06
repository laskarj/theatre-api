from rest_framework import serializers

from theatre.models import (
    Artist,
    Genre,
    Play,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
        )


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "about"
        )


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "genres",
            "acts",
            "description",
            "artists",
        )


class PlayListSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "genres",
            "acts",
        )


class PlayDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    artists = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "genres",
            "acts",
            "description",
            "artists",
        )


class PlayListForArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = ("id", "title", )


class ArtistDetailSerializer(serializers.ModelSerializer):
    plays = PlayDetailForArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ("id", "first_name", "last_name", "about", "plays", )
