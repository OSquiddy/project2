from django.contrib import admin

from .models import User, Listing, Comment, Bid, WatchList


# Register your models here.


class BidAdmin(admin.ModelAdmin):
    # readonly_fields = ['user', 'listing', 'price', 'winning_Bid', 'datetime']
    date_hierarchy = 'datetime'
    ordering = ['-datetime']
    search_fields = ['user__username', 'listing__title']
    list_display = ['user', 'listing', 'price', 'winning_Bid', 'datetime']

class ListingAdmin(admin.ModelAdmin):        
    list_display = ['title', 'cat1', 'condition', 'active', 'user', 'date']
    search_fields = ['title', 'user__username']
    ordering = ['id']

class UserAdmin(admin.ModelAdmin):        
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username']
    ordering = ['id']

class CommentAdmin(admin.ModelAdmin):        
    list_display = ['user', 'listing', 'comment', 'datetime']
    search_fields = ['user__username']

class WatchListAdmin(admin.ModelAdmin):        
    list_display = ['user']
    filter_horizontal = ['listings']
    search_fields = ['user__username']
    ordering = ['id']

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(WatchList, WatchListAdmin)

