# Generated by Django 5.1.1 on 2024-09-05 23:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("voting", "0006_remove_vote_weight"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vote",
            old_name="restaurant_id",
            new_name="restaurant",
        ),
    ]
