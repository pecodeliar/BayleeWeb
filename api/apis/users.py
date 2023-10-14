from auctions.models import User, Auction, Comment
from api.serializers.users import UserSerializer, RegisterSerializer, LoginSerializer
from api.serializers.listings import AuctionSerializer, CommentSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from knox.models import AuthToken
from api.permissions import IsOwner, IsSuperUser
from django.contrib.auth import login
from rest_framework.decorators import action




@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
    })

class UserPermission(permissions.BasePermission):

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
            return obj == request.user or request.user.is_staff
        else:
            return False


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions Allow user to retreive their own data if authenticated but otherwise must be admin.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    @action(detail=False, methods=['GET'], url_path='(?P<user_id>\d+)/listings', permission_classes=[permissions.AllowAny])
    def listings(self, request, user_id, *args, **kwargs):
        """This for getting all the listings of a particular user."""

        users = self.get_queryset()
        user = users.get(pk=user_id)
        posts = Auction.objects.filter(creator=user).order_by("-creation_date").all()
        results = AuctionSerializer(posts, many=True).data
        return Response(results)
    
    @action(detail=False, methods=['GET'], url_path='(?P<user_id>\d+)/comments', permission_classes=[permissions.AllowAny])
    def comments(self, request, user_id, *args, **kwargs):
        # This for getting all the comments made by a user

        users = self.get_queryset()
        user = users.get(pk=user_id)
        comments = Comment.objects.filter(creator=user).order_by("-creation_date").all()
        results = CommentSerializer(comments, many=True).data
        return Response(results)


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        login(request, user)
        return Response({
            "users": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1]
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

