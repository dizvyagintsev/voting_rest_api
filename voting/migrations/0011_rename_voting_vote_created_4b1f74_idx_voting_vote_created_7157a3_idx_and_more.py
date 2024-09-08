# Generated by Django 5.1.1 on 2024-09-08 05:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("voting", "0010_remove_vote_voting_vote_user_id_7dac28_idx_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="vote",
            new_name="voting_vote_created_7157a3_idx",
            old_name="voting_vote_created_4b1f74_idx",
        ),
        migrations.AlterField(
            model_name="vote",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
