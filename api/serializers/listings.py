from rest_framework import serializers
from auctions.models import Auction, Bid, Comment, User

class UserPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

class AuctionSerializer(serializers.ModelSerializer):
    creator = UserPKField(read_only=True, default=serializers.CurrentUserDefault())
    starting_price = serializers.DecimalField(decimal_places=2, max_digits=12)
    watchers = UserPKField(many=True, read_only=True)
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


    def validate_starting_price(self, value):                                     
        if self.instance and value != self.instance.starting_price:
            raise serializers.ValidationError("A starting price cannot be changed once auction is created.")
        return value


class BidSerializer(serializers.ModelSerializer):
    auction = serializers.SerializerMethodField()
    creator = UserPKField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Bid
        fields = [
            "id", 
            "creator",
            "auction",
            "price",
            "timestamp"
        ]

    def get_auction(self, obj):
        return self.context.get("auction_id")
    
    def validate(self, data):
        if self.context['request'].method == "POST":
            listing = Auction.objects.get(pk=self.context.get("auction_id"))
            # Checking to see if bidder is the owner of auction
            if listing.creator == self.context['request'].user:
                raise serializers.ValidationError("You cannot bid on your own auction.")
            # Checking to see if new bid is not lower than any other bids or starting price
            starting_price = listing.starting_price
            try:
                highest_bid = Bid.objects.get(auction=self.context.get("auction_id")).order_by('-price').first()
            except Bid.DoesNotExist:
                pass
            else:
                if data["price"] <= highest_bid:
                    raise serializers.ValidationError("Your bid needs to be higher than the current bid price.")
            if data["price"] <= starting_price:
                    raise serializers.ValidationError("Your bid needs to be higher than the current bid price.")
        return data


class CommentSerializer(serializers.ModelSerializer):
    auction = serializers.SerializerMethodField()
    creator = UserPKField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = [
            "id", 
            "creator",
            "auction",
            "text",
            "timestamp"
        ]

    def get_auction(self, obj):
        return self.context.get("auction_id")