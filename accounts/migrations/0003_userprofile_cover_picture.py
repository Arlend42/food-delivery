# Generated by Django 4.1.2 on 2022-11-14 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_rename_user_name_user_username_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="cover_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="user/cover_pictures"
            ),
        ),
    ]
