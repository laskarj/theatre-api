from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Artist
from theatre.serializers import ArtistListSerializer, ArtistDetailSerializer

ARTISTS_BASE_URL = reverse("theatre:artist-list")


def sample_artist(**params) -> Artist:
    defaults = {
        "first_name": "Sample_First",
        "last_name": "Sample_Last",
        "about": "Long text sample field",
    }
    defaults.update(**params)
    return Artist.objects.create(**defaults)

def detail_artist_url(artist_id) -> str:
    return reverse("theatre:artist-detail", args=[artist_id])


class UnauthenticatedArtistsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_artists_list(self):
        sample_artist()
        sample_artist()

        response = self.client.get(ARTISTS_BASE_URL, data={"page": 1})

        artists = Artist.objects.all()
        serializer = ArtistListSerializer(artists, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_artists_filtering_by_full_name(self):
        artist1 = sample_artist(first_name="First1", last_name="Last1")
        artist2 = sample_artist(first_name="First2", last_name="Last2")

        response = self.client.get(
            ARTISTS_BASE_URL,
            {"search_by": f"{artist1.first_name} {artist1.last_name}"},
        )

        serializer1 = ArtistListSerializer(artist1)
        serializer2 = ArtistListSerializer(artist2)

        self.assertIn(serializer1.data, response.data["results"])
        self.assertNotIn(serializer2.data, response.data["results"])

    def test_artists_filtering_by_first_name(self):
        artist1 = sample_artist(first_name="First1", last_name="Last1")
        artist2 = sample_artist(first_name="First2", last_name="Last2")

        response = self.client.get(
            ARTISTS_BASE_URL,
            {"search_by": artist1.first_name},
        )

        serializer1 = ArtistListSerializer(artist1)
        serializer2 = ArtistListSerializer(artist2)

        self.assertIn(serializer1.data, response.data["results"])
        self.assertNotIn(serializer2.data, response.data["results"])

    def test_artists_filtering_by_last_name(self):
        artist1 = sample_artist(first_name="First1", last_name="Last1")
        artist2 = sample_artist(first_name="First2", last_name="Last2")

        response = self.client.get(
            ARTISTS_BASE_URL,
            {"search_by": artist1.last_name},
        )

        serializer1 = ArtistListSerializer(artist1)
        serializer2 = ArtistListSerializer(artist2)

        self.assertIn(serializer1.data, response.data["results"])
        self.assertNotIn(serializer2.data, response.data["results"])

    def test_artist_filtering_by_partial_identifiers(self):
        artist1 = sample_artist(first_name="First1", last_name="Last1")
        artist2 = sample_artist(first_name="First2", last_name="Last2")

        response = self.client.get(
            ARTISTS_BASE_URL,
            {"search_by": "fir las"},
        )

        serializer1 = ArtistListSerializer(artist1)
        serializer2 = ArtistListSerializer(artist2)

        self.assertIn(serializer1.data, response.data["results"])
        self.assertIn(serializer2.data, response.data["results"])

    def test_retrieve_artist_detail(self):
        artist = sample_artist()

        url = detail_artist_url(artist.id)
        response = self.client.get(url)

        serializer = ArtistDetailSerializer(artist)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
