# Generated by Django 5.1.1 on 2024-09-05 20:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("voting", "0003_remove_vote_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="vote",
            name="weight",
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name="vote",
            index=models.Index(
                fields=["user_id", "created_at"], name="voting_vote_user_id_d468f5_idx"
            ),
        ),
    ]
