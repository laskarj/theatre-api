from django.contrib import admin

from theatre.models import (
    Artist,
    Genre,
    Play,
    Performance,
    TheatreHall,
    Reservation,
    Ticket
)

admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Play)
admin.site.register(Performance)
admin.site.register(TheatreHall)
admin.site.register(Reservation)
admin.site.register(Ticket)
