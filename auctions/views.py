from django.shortcuts import render
from django.contrib.auth import logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import F
from django.contrib.auth.decorators import login_required
import random

from .models import User, Auction, Bid, Comment



# Create your views here.
def login(request):

    return render(request, "auctions/login.html", {
            "page": "Login"
        })

    """if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("common:index"))
    else:
        return render(request, "users/auth.html", {
            "page": "Login"
        })"""


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:login"))


def register(request):

    return render(request, "auctions/register.html", {
            "page": "Register"
        })

    """if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("common:index"))
    else:
        return render(request, "users/auth.html", {
            "page": "Register"
        })"""
    
class ListingForm(forms.Form):
    """Image comes after text fields."""
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))
    description = forms.CharField(label='Item Description', widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))
    price = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))
    image_link = forms.URLField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))


class BidForm(forms.Form):
    bid = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(attrs={'class': 'bid-form-box'}))


class CommentForm(forms.Form):
    comment = forms.CharField(label='Comment', widget=forms.TextInput(attrs={'class': 'comment-form-box'}))


class ManageAccountForm(forms.Form):
    first_name = forms.CharField(label='First Name', required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))
    username = forms.CharField(label='Username', required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))
    email = forms.CharField(label='Email', required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))
    profile_picture = forms.URLField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))
    pfp_credit = forms.CharField(label='Profile Picture Credit', required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))
    banner = forms.URLField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))
    banner_credit = forms.CharField(label='Banner Credit', required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-none log-reg-inp mng-inp'}))


def index(request):

    listings = []
    items = sorted(Auction.objects.filter(active=True).all(), key=lambda x: random.random())
    for item in items:
        listing = {}
        listing["details"] = item
        listing["highest_bid"] = Bid.objects.filter(auction=item.id).order_by('-price').first()
        listings.append(listing)
    return render(request, "auctions/index.html", {
    "listings": listings
})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


@login_required
def create_listing(request):
    return render(request, "auctions/create.html", {
            "form_fields": list(ListingForm())
        })

def visit_listing(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)

    user_is_highest_bidder = False

   # The listing does not exist.
    if listing == None:
       return render(request, "auctions/index.html", {
        "listings": Auction.objects.all()
        })

    # Find if there are comments for listing
    comments = Comment.objects.filter(auction=listing).order_by("timestamp").all()
    comment_count = comments.count()

    # Find if listings has bids
    bids = Bid.objects.filter(auction=listing).order_by("timestamp").all()
    bid_count = bids.count()
    if bid_count != 0:
        highest_bid = bids.order_by('-price').first()

    # Check if a user is logged in
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)

        # Check if logged in user has highest bid
        if bid_count != 0 and user == highest_bid.creator:
            user_is_highest_bidder = True


    if request.method == "POST":

        # The Closed button was pressed by creator
        if "close_auction_button" in request.POST.keys():
            # https://docs.djangoproject.com/en/4.1/ref/forms/api/#accessing-clean-data
            listing.active = False
            listing.save()
            return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))

    else:
        # GET method
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_form": BidForm(),
            "bid_count": bid_count,
            "bid_apology": False,
            "highest_bidder": user_is_highest_bidder,
            "bid_history": bids,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": CommentForm()
        })


@login_required
def watchlist(request):
    auctions = Auction.objects.filter(watchers=request.user.pk).all()
    return render(request, "auctions/watchlist.html", {
        "listings": auctions
    })


@login_required
def manage(request):

    user = User.objects.get(pk=request.user.pk)

    default_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'profile_picture': user.profile_picture,
        'pfp_credit': user.pfp_credit,
        'banner': user.banner,
        'banner_credit': user.banner_credit
        }
    # https://stackoverflow.com/questions/65833407/divide-django-form-fields-to-two-divs
    return render(request, "auctions/manage.html", {
        "form_fields": list(ManageAccountForm(default_data))
    })


def account(request, user_id):
    account = User.objects.get(pk=user_id)

    # Find if user has made any comments
    comments = Comment.objects.filter(creator=account)

    # Find if user has made any auctions
    auctions = Auction.objects.filter(creator_id=account)

    return render(request, "auctions/profile.html", {
        "account": account,
        "comments": comments,
        "listings": auctions
    })


@login_required
def edit(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)

    # Check if there have been bids
    bid_count = Bid.objects.filter(auction=listing).count()
        
    # GET method
    default_data = {
        'title': listing.title,
        'description': listing.description,
        'price': listing.starting_price,
        'image_link': listing.image,
        }
    # https://stackoverflow.com/questions/65833407/divide-django-form-fields-to-two-divs
    return render(request, "auctions/edit.html", {
        "listing": listing,
        "form_fields": list(ListingForm(default_data)),
        "bid_count": bid_count
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category(request, category_id):
    return render(request, "auctions/category.html", {
        "listings": Auction.objects.filter(category_id=category_id, active=True).all(),
        "category_name": Category.objects.get(pk=category_id).name
    })