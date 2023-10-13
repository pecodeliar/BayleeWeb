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

    return render(request, "users/auth.html", {
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
    return HttpResponseRedirect(reverse("auth:login"))


def register(request):

    return render(request, "users/auth.html", {
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

    if request.method == "POST":
        # User is switch themes
        if "theme_button" in request.POST.keys():
            theme_switch(User.objects.get(pk=request.user.pk), request.POST["theme_button"])
            return HttpResponseRedirect(reverse("auctions:index"))
    else:
        items = sorted(Auction.objects.filter(active=True).all(), key=lambda x: random.random())
        return render(request, "auctions/index.html", {
        "listings": items
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, last_name=last_name, first_name=first_name)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        # User is switch themes
        if "theme_button" in request.POST.keys():
            theme_switch(User.objects.get(pk=request.user.pk), request.POST["theme_button"])
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

        form = ListingForm(request.POST)
        if form.is_valid():
            # https://docs.djangoproject.com/en/4.1/topics/auth/customizing/
            creator = User.objects.get(pk=request.user.pk)

            # Not to self: Should I check for a duplicate listing?
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            category_id = request.POST["category"]
            category = Category.objects.get(pk=category_id)

            image_link = form.cleaned_data['image_link']
            # https://docs.djangoproject.com/en/4.1/topics/db/queries/
            new_listing = Auction(creator_id=creator, title=title, description=description, price=price, image_link=image_link, category_id=category)
            new_listing.save()
            return render(request, "auctions/account.html", {
                    "account": creator,
                    "comments": Comment.objects.filter(user=creator),
                    "listings": Auction.objects.filter(creator_id=creator)
                })
    else:
        return render(request, "auctions/create.html", {
            "form_fields": list(ListingForm()),
            "categories": Category.objects.all()
        })

def visit_listing(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)

    watchers = listing.watchers.all()
    user_is_watcher = False
    user_is_highest_bidder = False
    user_is_creator = False

   # The listing does not exist.
    if listing == None:
       return render(request, "auctions/index.html", {
        "listings": Auction.objects.all()
        })

    # Find if there are comments for listing
    comments = Comment.objects.filter(auction=listing)
    comment_count = comments.count()

    # Find if listings has bids
    bids = Bid.objects.filter(auction=listing)
    bid_count = bids.count()
    if bid_count != 0:
        highest_bid = bids.order_by('-price').first()

    # Check if a user is logged in
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)

        # Check if user is the creator
        if user == listing.creator_id:
            user_is_creator = True

        # Check if user is watcher
        if user in watchers:
            user_is_watcher = True

        # Check if logged in user has highest bid
        if bid_count != 0 and user == highest_bid.user:
            user_is_highest_bidder = True


    if request.method == "POST":
        # User is switch themes
        if "theme_button" in request.POST.keys():
            theme_switch(user, request.POST["theme_button"])
            return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))

        # The Watchlist button was pressed
        if "watchlist_button" in request.POST.keys():
            # https://docs.djangoproject.com/en/4.1/ref/forms/api/#accessing-clean-data
            option = request.POST["watchlist_button"]
            if option == "Add to Watchlist":
                listing.watchers.add(user)
                return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
            elif option == "Remove From Watchlist":
                listing.watchers.remove(user)
                return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))

        # The Closed button was pressed by creator
        if "close_auction_button" in request.POST.keys():
            # https://docs.djangoproject.com/en/4.1/ref/forms/api/#accessing-clean-data
            listing.active = False
            listing.save()
            return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))

        # The User is trying to place a bid by pressing Place Bid button
        if "place_bid_button" in request.POST.keys():
            form = BidForm(request.POST)
            if form.is_valid():

                bid = form.cleaned_data['bid']

                # Bid is lower than highest bid or price
                if bid <= listing.price:
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "bid_form": BidForm(),
                        "bid_apology": True,
                        "in_watchlist": user_is_watcher,
                        "highest_bidder": user_is_highest_bidder,
                        "creator_logged_in": user_is_creator,
                        "comments": comments,
                        "comment_count": comment_count,
                        "comment_form": CommentForm()
                    })
                else:
                    # https://docs.djangoproject.com/en/4.1/ref/models/instances/#updating-attributes-based-on-existing-fields
                    listing.price = bid
                    listing.save()

                    new_bid = Bid(auction=listing, user=user, price=bid)
                    new_bid.save()
                    return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))

        # The User is trying to ass a comment using the Add Comment button
        if "add_comment_button" in request.POST.keys():

            form = CommentForm(request.POST)
            if form.is_valid():

                comment = form.cleaned_data['comment']
                new_comment = Comment(auction=listing, user=user, text=comment)
                new_comment.save()
                return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
    else:
        # GET method
        return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bid_form": BidForm(),
                    "bid_count": bid_count,
                    "bid_apology": False,
                    "in_watchlist": user_is_watcher,
                    "highest_bidder": user_is_highest_bidder,
                    "creator_logged_in": user_is_creator,
                    "comments": comments,
                    "comment_count": comment_count,
                    "comment_form": CommentForm()
                })


@login_required
def watchlist(request):
    if request.method == "POST":
        # User is switch themes
        if "theme_button" in request.POST.keys():
            theme_switch(User.objects.get(pk=request.user.pk), request.POST["theme_button"])
            return HttpResponseRedirect(reverse("auctions:watchlist"))
    else:
        auctions = Auction.objects.filter(watchers=request.user.pk).all()
        return render(request, "auctions/watchlist.html", {
            "listings": auctions
        })


@login_required
def manage(request):

    user = User.objects.get(pk=request.user.pk)

    if request.method == "POST":
        # User is switch themes
        if "theme_button" in request.POST.keys():
            theme_switch(User.objects.get(pk=request.user.pk), request.POST["theme_button"])
            return HttpResponseRedirect(reverse("auctions:manage"))

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        profile_picture = request.POST["profile_picture"]
        pfp_credit = request.POST["pfp_credit"]
        banner = request.POST["banner"]
        banner_credit = request.POST["banner_credit"]

        try:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.profile_picture = profile_picture
            user.pfp_credit = pfp_credit
            user.banner = banner
            user.banner_credit = banner_credit
            user.save()
        except IntegrityError:
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
            return render(request, "auctions/manage.html", {
                "message": "Username already taken.",
                "form_fields": list(ManageAccountForm(default_data))
            })

        return HttpResponseRedirect(reverse("auctions:account", args=(user.id,)))

    else:
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
    comments = Comment.objects.filter(user=account)

    # Find if user has made any auctions
    auctions = Auction.objects.filter(creator_id=account)

    if request.method == "POST":
        # User is switch themes
        if "theme_button" in request.POST.keys():
            theme_switch(User.objects.get(pk=request.user.pk), request.POST["theme_button"])
            return HttpResponseRedirect(reverse("auctions:account", args=(account.id,)))
    else:
        return render(request, "auctions/account.html", {
                    "account": account,
                    "comments": comments,
                    "listings": auctions
                })


@login_required
def edit(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)

    # Check if there have been bids
    bid_count = Bid.objects.filter(auction=listing).count()

    # Make sure that logged in user is creator
    is_creator = False
    user = User.objects.get(pk=request.user.pk)
    if user == listing.creator_id:
        is_creator = True

    if request.method == "POST":

        # User is switch themes
        if "theme_button" in request.POST.keys():
            theme_switch(User.objects.get(pk=request.user.pk), request.POST["theme_button"])
            return HttpResponseRedirect(reverse("auctions:edit", args=(listing.id,)))

        # User submitted changes for listing by pressing Save Changes button

        if "save_edit_button" in request.POST.keys():
            form = ListingForm(request.POST)
            if form.is_valid():
                # Bids have not been placed on the listing
                if bid_count == 0:
                    listing.title = form.cleaned_data['title']
                    listing.description = form.cleaned_data['description']
                    listing.price = form.cleaned_data['price']
                    listing.image_link = form.cleaned_data['image_link']

                    category_id = request.POST["category"]
                    listing.category = Category.objects.get(pk=category_id)

                    listing.save()
                    return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
                # Bids have been placed so the user should not be able to change it anymore
                else:
                    listing.title = form.cleaned_data['title']
                    listing.description = form.cleaned_data['description']
                    listing.image_link = form.cleaned_data['image_link']

                    category_id = request.POST["category"]
                    listing.category = Category.objects.get(pk=category_id)

                    listing.save()
                    return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
            else:
                # Something went wrong
                return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
    else:
        # GET method
        default_data = {
            'title': listing.title,
            'description': listing.description,
            'price': listing.price,
            'image_link': listing.image_link,
            }
        # https://stackoverflow.com/questions/65833407/divide-django-form-fields-to-two-divs
        return render(request, "auctions/edit.html", {
                    "listing": listing,
                    "form_fields": list(ListingForm(default_data)),
                    "categories": Category.objects.all(),
                    "is_creator": is_creator,
                    "category_id": listing.category_id,
                    "bid_count": bid_count
                })


def categories(request):
    if request.method == "POST":
        # User is switch themes
        if "theme_button" in request.POST.keys():
            theme_switch(User.objects.get(pk=request.user.pk), request.POST["theme_button"])
            return HttpResponseRedirect(reverse("auctions:categories"))
    else:
        return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category(request, category_id):
    if request.method == "POST":
        # User is switch themes
        if "theme_button" in request.POST.keys():
            theme_switch(User.objects.get(pk=request.user.pk), request.POST["theme_button"])
            return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/category.html", {
        "listings": Auction.objects.filter(category_id=category_id, active=True).all(),
        "category_name": Category.objects.get(pk=category_id).name
    })


def theme_switch(user, switch_request):
    option = switch_request
    if option == "Switch to Dark Mode":
        user.dark_theme = True
        user.save()
    elif option == "Switch to Light Mode":
        user.dark_theme = False
        user.save()