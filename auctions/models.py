from django.contrib.auth.models import AbstractUser
from django.db import models
import django


class User(AbstractUser):
    profile_picture = models.URLField(blank=True, null=True)
    pfp_credit = models.CharField(max_length=64, blank=True, null=True)
    banner = models.URLField(blank=True, null=True)
    banner_credit = models.CharField(max_length=64, blank=True, null=True)


# One User can have Many Auction Listings (O->M)
class Auction(models.Model):
    class Category(models.IntegerChoices):
        # https://stackoverflow.com/questions/18676156/how-to-properly-use-the-choices-field-option-in-django
        OTHER = 0, "Other"
        FASHION = 1, "Fashion"
        TOYS = 2, "Toys"
        ELECTRONICS = 3, "Electronics"
        HOME = 4, "Home"
        WEAPONS = 5, "Weapons"
        HOBBY = 6, "Hobby"
        BEAUTY = 7, "Beauty"
        KITCHEN = 8, "Kitchen"

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    starting_price = models.DecimalField(decimal_places=2, max_digits=12)
    image = models.URLField(blank=True, null=True)
    category = models.PositiveSmallIntegerField(
        choices=Category.choices,
        default=Category.OTHER
    )
    creation_date = models.DateField(auto_now=True)
    creation_time = models.TimeField(auto_now=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="auction_watchers")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# One Auction can have Many Bids (O->M)
class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_bid")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_creator")
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)


# One Auction can have many comments (O->M)
class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_comment")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_creator")
    text = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)

