from django.contrib.auth.models import AbstractUser
from django.db import models
from sqlalchemy import ForeignKey
from datetime import datetime


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(null=True, max_length=300)
    starting_price = models.FloatField()
    URL_image = models.CharField(max_length=400, null=True, blank=True)
    category = models.CharField(max_length=64, null=True, blank=True)
    current_state = models.BooleanField(default=True)
    current_price = models.FloatField(null=True, blank=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(User, blank=True, related_name="users_watchlist")
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.id} {self.title} {self.description}"

class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="comment")
    comments = models.CharField(max_length=300)
    time = models.DateTimeField(default=datetime.now)

class Bids(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    bid = models.FloatField()
    winner = models.BooleanField(default=False)
    time = models.DateTimeField(default=datetime.now)