import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


def object_image_file_path(
        instance: models.Model,
        filename: str
) -> str:
    """
    Upload an image to object storage.
    Call __str__ to get an image name from instance
    """
    directory = str(instance._meta.verbose_name_plural)
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.__str__())}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", directory, filename)


class Artist(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    about = models.TextField(blank=True)
    image = models.ImageField(upload_to=object_image_file_path, null=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(
        Genre, blank=True, related_name="plays"
    )
    artists = models.ManyToManyField(
        Artist, blank=True, related_name="plays"
    )
    acts = models.IntegerField(default=1)

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.CASCADE, related_name="performances"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField()
    image = models.ImageField(
        upload_to=object_image_file_path, null=True
    )

    class Meta:
        ordering = ("-show_time",)

    def __str__(self):
        return f"{self.play.title} {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ("-created_at",)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    @staticmethod
    def validate_tickets(
            row: int,
            seat: int,
            theater_hall: TheatreHall,
            error_to_raise: ValidationError
    ) -> None:
        for ticket_attr_value, ticket_attr_name, theater_hall_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row")
        ]:
            count_attrs = getattr(theater_hall, theater_hall_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        "number must be in available range: "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self) -> None:
        Ticket.validate_tickets(
            self.row,
            self.seat,
            self.performance.theatre_hall,
            ValidationError
        )

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using=None,
            update_fields=None
    ) -> models.Model:
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    class Meta:
        unique_together = (
            "performance",
            "row",
            "seat",
        )
        ordering = (
            "row",
            "seat",
        )

    def __str__(self):
        return f"{str(self.performance)} (row: {self.row}, seat: {self.seat})"
