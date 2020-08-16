from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime

class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"

class ListingManager(models.Manager):
    def create_listing(self, user, title, url, cat1, cat2, cat3, condition, description, start_price):
        listing = self.create(user=user, title=title, url=url, cat1=cat1, cat2=cat2, cat3=cat3, condition=condition, description=description, start_price=start_price)
        return listing

# 1st Additional Model
class Listing(models.Model):
    ELECTRONICS = 'el'
    SPORTS = 'sp'
    EDUCATION = 'ed'
    BOOKS = 'bk'
    TOYS = 'ty'
    ART = 'ar'
    CLOTHES = 'cl'
    BEAUTY= 'bf'
    HOME = 'hm'
    ACCESSORIES = 'ac'
    LUXURY = 'lx'
    JEWELLERY = 'jw'
    choices = [
        ( "", ""),
        (ELECTRONICS, 'Electronics'),
        (SPORTS, 'Sports'),
        (EDUCATION, 'Education'),
        (TOYS, 'Toys'),
        (BOOKS, 'Books'),
        (ART, 'Art'),
        (LUXURY, 'Luxury'),
        (CLOTHES, 'Clothes'),
        (JEWELLERY, 'Jewellery'),
        (BEAUTY, 'Beauty and Fragrances'),
        (HOME, 'Home'),
        (ACCESSORIES, 'Accessories')
    ]
    
    NEW = "bn"
    USED_ONCE = "u1"
    USED = "us"
    condition_choices = [
        ("", ""),
        (NEW, "Brand New"),
        (USED_ONCE, "Used once"),
        (USED, 'Used')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listings")
    title = models.CharField(max_length=128)
    date = models.DateField(auto_now_add=True)
    url = models.URLField(blank=True)
    cat1 = models.CharField(blank=True, max_length=2, choices=choices)
    cat2 = models.CharField(blank=True, max_length=2, choices=choices)
    cat3 = models.CharField(blank=True, max_length=2, choices=choices)
    description = models.TextField()
    condition = models.CharField(blank=True, max_length=2, choices=condition_choices)
    start_price = models.DecimalField(max_digits=10, decimal_places=0)

    active = models.BooleanField(default=True)

    objects = ListingManager()

    def __str__(self):
        answer = f"{self.title} : {self.start_price}"
        if self.cat1 != '':
            answer += f", {self.cat1}"
        if self.cat2 != '':
            answer += f", {self.cat2}"
        if self.cat3 != '':
            answer += f", {self.cat3}"
        return answer

# 2nd Additional Model
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="bids")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    winning_Bid = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f"Bid by user({self.user}) for listing({self.listing.title}) : ${self.price} | Last modified: {self.datetime}"

# 3rd Additional Model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comments")
    comment = models.TextField(blank=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    ordering = ['-datetime',]

    def __str__(self):
        return f"Comment by user['{self.user}'] for listing['{self.listing}']"

class WatchListManager(models.Manager):
    def create_watchlist(self, user):
        wl = self.create(user = user)
        return wl

# 4th Additional Model 
class WatchList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    listings = models.ManyToManyField(Listing, related_name="watchlist")

    objects = WatchListManager()

    def __str__(self):
        return f"{self.user}'s Watchlist"