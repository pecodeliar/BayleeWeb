from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .apis import listings, users
from knox import views as knox_views

router = DefaultRouter()
router.register(r"users", users.UserViewSet, basename="users_api")
router.register(r"listings", listings.AuctionViewSet, basename="listings_api")
# https://stackoverflow.com/questions/63439268/how-to-use-parameters-in-drf-router
router.register(r"listings/(?P<auction_id>\d+)/bids", listings.BidViewSet, basename="bids_api")
router.register(r"listings/(?P<auction_id>\d+)/comments", listings.CommentViewSet, basename="comments_api")


urlpatterns = [
    path("listings/<int:listing_id>/watch", listings.watch, name="watch_action"),

    # User (Knox) Routes
    path('', include(router.urls)),
    #path('users/<int:pk>/update', users.UserUpdateView.as_view()),
    #path('users/<int:pk>/deactivate', users.UserDeactivateView.as_view()),
    path('auth-api/', include('knox.urls')),
    path('logout', knox_views.LogoutView.as_view(), name="knox-logout"),
    path('register', users.RegisterView.as_view()),
    path('login', users.LoginView.as_view()),
]