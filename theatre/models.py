import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.text import slugify


def object_image_file_path(
        instance: models.Model,
        filename: str
) -> str:
    """
    Upload an image to object storage.
    Call __str__ to get an image name from instance
    """
    directory = instance._meta.verbose_name_plural
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance)}-{uuid.uuid4()}{extension}"

    return os.path.join(f"uploads/{directory}/", filename)


class Artist(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    about = models.TextField(blank=True)
    image = models.ImageField(upload_to=object_image_file_path, blank=True)

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
    seat_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seat_in_row

    def __str__(self) -> str:
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        ordering = ("-show_time",)

    def __str__(self):
        return self.play.title + " " + str(self.show_time)


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ("-created_at",)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

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
        return f"{str(self.movie_session)} (row: {self.row}, seat: {self.seat})"
