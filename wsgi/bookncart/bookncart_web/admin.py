from django.contrib import admin

from .models import *

admin.site.register(Tags)
admin.site.register(Reviews)
admin.site.register(User_cart)
admin.site.register(User_wishlist)
admin.site.register(Address)
admin.site.register(Location)
admin.site.register(Orders)
admin.site.register(Books_ordered)
admin.site.register(Banners)
admin.site.register(Recently_viewed_books)
admin.site.register(UserProfileBackgroundImages)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_id')
    list_filter = ['parent_id']
    search_fields = ['name']


admin.site.register(Categories, CategoriesAdmin)


class BooksAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'mrp', 'price', 'stock', 'is_featured', 'view_count', 'sell_count', 'condition_is_old', 'edition')
    list_filter = ['mrp', 'price', 'stock', 'is_featured', 'view_count', 'sell_count', 'condition_is_old', 'tags_id']
    search_fields = ['name']


admin.site.register(Books, BooksAdmin)


class UserProfilesAdmin(admin.ModelAdmin):
    readonly_fields = ('account_creation_date', 'last_login')


admin.site.register(UserProfiles, UserProfilesAdmin)
