from auctions.models import Auction, Bid, Comment
from api.serializers.listings import AuctionSerializer, BidSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework import status, permissions, viewsets
from api.permissions import IsOwner
from rest_framework import generics

class IsOwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user and request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):

        if view.action == 'retrieve':
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return obj.creator == request.user or request.user.is_staff
        else:
            return False


class AuctionViewSet(viewsets.ModelViewSet):
    serializer_class = AuctionSerializer
    permission_classes = [IsOwnerPermission]


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


    def get_queryset(self):
        """
        This view should return a list of all the auctions
        for the currently authenticated user.
        """
        user = self.request.user
        #return Auction.objects.filter(creator=user)
        return Auction.objects.all()

    @action(detail=True)
    def auction_detail(self, request, pk):
        """
        This view should return details for an auction 
        but should only allow editing if authenticated user made the listing.
        """
        serializer = self.get_serializer(data=request.data)
        auction = self.get_object()
        user = self.request.user
        #if self.request.method == "POST" and auction.creator != user:
            #return Response(serializer.errors, status=status.HTTP_405_NOT_ALLOWED)
        return Response(AuctionSerializer(auction).data)
    
    @action(detail=False, methods=['GET'], url_path='watchlist', permission_classes=[permissions.IsAuthenticated])
    def watchlist(self, request, *args, **kwargs):
        """This is for getting all the listings the logged in user is watching."""

        listings = Auction.objects.filter(watchers__id=request.user.pk).order_by("-creation_date").all()
        results = AuctionSerializer(listings, many=True).data
        return Response(results)


@api_view(['GET', 'PATCH'])
def watch(request, listing_id):
    """This function is for watching a listing.
    This is to avoid having to make a completely seperate model for watchers/watchlist."""
    data = request.data
    if request.method == 'PATCH':

        if data.get("action") not in ["Add", "Remove"]:
            content = {"error": "You can only Add or Remove"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        listing = Auction.objects.get(pk=listing_id)
        if data.get("action") == "Add":
            listing.watchers.add(request.user.id)
            listing.save()
            watchers = list(listing.watchers.all().values_list('pk', flat=True))
            return Response(watchers)
        elif data.get("action") == "Remove":
            listing.watchers.remove(request.user.id)
            listing.save()
            watchers = list(listing.watchers.all().values_list('pk', flat=True))
            return Response(watchers)
        else:
            content = {"error": "Must to be a listing."}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "GET or PATCH request required."}, status=status.HTTP_400_BAD_REQUEST)
    

class BidView(generics.CreateAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Bid.objects.all()

    # https://stackoverflow.com/questions/54983239/pass-url-parameter-to-serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "auction_id": int(self.kwargs['auction_id'])
            }
        )
        return context


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


    def get_queryset(self):
        """
        This view should return a list of all the auctions
        for the currently authenticated user.
        """
        user = self.request.user
        return Bid.objects.filter(creator=user)

    @action(detail=True)
    def auction_detail(self, request, pk):
        """
        This view should return details for an auction
        for the currently authenticated user that created the activity.
        """
        serializer = self.get_serializer(data=request.data)
        bid = self.get_object()
        user = self.request.user
        if self.request.method == "POST" and auction.creator != user:
            return Response(serializer.errors, status=status.HTTP_405_NOT_ALLOWED)
        return Response(AuctionSerializer(auction).data)
    

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # https://stackoverflow.com/questions/54983239/pass-url-parameter-to-serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "auction_id": int(self.kwargs['auction_id'])
            }
        )
        return context


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


    def get_queryset(self):
        """
        This view should return a list of all the comments
        for the currently authenticated user.
        """
        user = self.request.user
        return Comment.objects.filter(creator=user)

    @action(detail=True)
    def auction_detail(self, request, pk):
        """
        This view should return details for an auction
        for the currently authenticated user that created the activity.
        """
        serializer = self.get_serializer(data=request.data)
        comment = self.get_object()
        user = self.request.user
        if self.request.method == "POST" and comment.creator != user:
            return Response(serializer.errors, status=status.HTTP_405_NOT_ALLOWED)
        return Response(CommentSerializer(comment).data)