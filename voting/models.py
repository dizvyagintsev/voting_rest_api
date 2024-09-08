from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    user_id = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at", "restaurant_id", "user_id"]),
            models.Index(fields=["created_at", "restaurant_id"]),
        ]

