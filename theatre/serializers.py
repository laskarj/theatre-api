from django.db import transaction
from django.db.models import Model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from theatre.models import (
    Artist,
    Genre,
    Performance,
    Play,
    Reservation,
    TheatreHall,
    Ticket,
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


class ArtistImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("id", "image", )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "image", )


def get_image_serializer(model_class: Model):
    class DynamicImageSerializer(ImageSerializer):
        class Meta(ImageSerializer.Meta):
            model = model_class
    return DynamicImageSerializer


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
    play_title = serializers.CharField(source="play.title", read_only=True)
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
            "play_title",
            "image",
            "theatre_hall_name",
            "theatre_hall_capacity",
            "tickets_available",
        )


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", )


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance", )

    def validate(self, attrs: dict) -> dict:
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_tickets(
            attrs["row"],
            attrs["seat"],
            attrs["performance"].theatre_hall,
            ValidationError
        )
        return data


class TicketListSerializer(TicketSerializer):
    performance = PerformanceListSerializer(many=False, read_only=True)


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


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(
        many=True, read_only=True, allow_empty=False
    )

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at", )

    def create(self, validated_data: dict) -> Reservation:
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = validated_data.pop("reservation")
            ticket_instances = [
                Ticket(**ticket_data)
                for ticket_data in tickets_data
            ]
            Ticket.objects.bulk_create(ticket_instances)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
