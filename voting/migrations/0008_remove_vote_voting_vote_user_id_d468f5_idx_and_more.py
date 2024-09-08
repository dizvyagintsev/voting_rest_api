# Generated by Django 5.1.1 on 2024-09-08 02:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("voting", "0007_rename_restaurant_id_vote_restaurant"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="vote",
            name="voting_vote_user_id_d468f5_idx",
        ),
        migrations.AddIndex(
            model_name="vote",
            index=models.Index(
                fields=["user_id", "restaurant", "created_at"],
                name="voting_vote_user_id_7dac28_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="vote",
            index=models.Index(
                fields=["restaurant"], name="voting_vote_restaur_6509c0_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="vote",
            index=models.Index(
                fields=["restaurant_id", "created_at"],
                name="voting_vote_restaur_22b5fd_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="vote",
            index=models.Index(
                fields=["created_at", "user_id", "restaurant_id"],
                name="voting_vote_created_efba96_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="vote",
            index=models.Index(
                fields=["created_at"], name="voting_vote_created_f40b96_idx"
            ),
        ),
    ]
