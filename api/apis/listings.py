from auctions.models import Auction, Bid, Comment
from api.serializers.listings import AuctionSerializer, BidSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework import status, permissions, viewsets
from api.permissions import IsOwner
from rest_framework import generics


class AuctionViewSet(viewsets.ModelViewSet):
    serializer_class = AuctionSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


    def get_queryset(self):
        """
        This view should return a list of all the auctions
        for the currently authenticated user.
        """
        user = self.request.user
        return Auction.objects.filter(creator=user)

    @action(detail=True)
    def auction_detail(self, request, pk):
        """
        This view should return details for an auction
        for the currently authenticated user that created the activity.
        """
        serializer = self.get_serializer(data=request.data)
        auction = self.get_object()
        user = self.request.user
        if self.request.method == "POST" and auction.creator != user:
            return Response(serializer.errors, status=status.HTTP_405_NOT_ALLOWED)
        return Response(AuctionSerializer(auction).data)
    

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