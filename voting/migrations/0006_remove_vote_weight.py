# Generated by Django 5.1.1 on 2024-09-05 23:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("voting", "0005_rename_restaurant_vote_restaurant_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vote",
            name="weight",
        ),
    ]
