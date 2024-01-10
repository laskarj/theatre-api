from rest_framework import serializers

from theatre.models import (
    Artist,
    Genre,
    Play,
    Performance,
    Ticket,
    TheatreHall,
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
            "about",
            "image",
        )


class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            "id",
            "full_name",
            "image",
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
    artists = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )

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
    plays = PlayListForArtistSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Artist
        fields = (
            "id",
            "first_name",
            "last_name",
            "about",
            "plays",
            "image",
        )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("id", "image", )


class PerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = (
            "id",
            "theatre_hall",
            "show_time",
            "image",
            "play"
        )


class PerformanceListSerializer(serializers.ModelSerializer):
    plays_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    theatre_hall_capacity = serializers.IntegerField(read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "show_time",
            "plays_title",
            "image",
            "theatre_hall_name",
            "theatre_hall_capacity",
            "tickets_available",
        )


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", )


class TicketSeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat", )


class PerformanceDetailSerializer(serializers.ModelSerializer):
    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )
    theatre_hall = TheatreHallSerializer(many=False, read_only=True)
    play = PlayListSerializer(many=False, read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "image",
            "show_time",
            "play",
            "theatre_hall",
            "taken_places",
        )
