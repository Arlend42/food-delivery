# Generated by Django 4.1.2 on 2022-11-18 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="restaurant_slug",
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
