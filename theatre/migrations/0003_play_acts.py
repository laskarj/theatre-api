# Generated by Django 5.0.1 on 2024-01-06 18:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("theatre", "0002_alter_reservation_options_alter_ticket_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="play",
            name="acts",
            field=models.IntegerField(default=1),
        ),
    ]
