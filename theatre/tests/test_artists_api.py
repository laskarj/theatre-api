from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Artist
from theatre.serializers import ArtistListSerializer


ARTISTS_BASE_API = reverse("theatre:artist-list")


def sample_artist(**params) -> Artist:
    defaults = {
        "first_name": "Sample_First",
        "last_name": "Sample_Last",
        "about": "Long text sample field",
    }
    defaults.update(**params)
    return Artist.objects.create(**defaults)


class UnauthenticatedArtistsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_artists_list(self):
        sample_artist()
        sample_artist()

        response = self.client.get(ARTISTS_BASE_API, data={"page": 1})

        artists = Artist.objects.all()
        serializer = ArtistListSerializer(artists, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)
