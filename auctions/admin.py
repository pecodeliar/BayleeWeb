from django.contrib import admin
from .models import User, Auction, Bid, Comment


class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "title", "description", "starting_price", "image", "creation_date", "creation_time")
    horizontal_display = ("watchers",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "text", "auction")


class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "creator", "price", "creation_date")



# Register your models here.
admin.site.register(User),
admin.site.register(Auction, AuctionAdmin),
admin.site.register(Bid, BidAdmin),
admin.site.register(Comment, CommentAdmin)