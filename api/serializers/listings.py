from rest_framework import serializers
from auctions.models import Auction, Bid, Comment


class AuctionSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Auction
        fields = [
            "id", 
            "creator",
            "title",
            "description",
            "starting_price",
            "image",
            "category",
            "creation_date",
            "creation_time",
            "watchers",
            "active"
        ]


class BidSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Bid
        fields = [
            "id", 
            "creator",
            "auction",
            "price",
            "creation_date"
        ]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = [
            "id", 
            "creator",
            "auction",
            "text"
            "creation_date"
        ]