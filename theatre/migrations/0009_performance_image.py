# Generated by Django 5.0.1 on 2024-01-10 15:00

import theatre.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("theatre", "0008_alter_play_options_artist_image_alter_play_genres"),
    ]

    operations = [
        migrations.AddField(
            model_name="performance",
            name="image",
            field=models.ImageField(
                blank=True, upload_to=theatre.models.object_image_file_path
            ),
        ),
    ]
