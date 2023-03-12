from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    model           = Profile
    list_display    = ('address', 'phone')
    search_fields   = ('id','phone', 'user__first__name', 'address',)

class BikeAdmin(admin.ModelAdmin):
    model           = Bike
    list_display    = ('serie_number', 'date_bought')
    search_fields   = ('id','serie_number',)

class UnlockPackageAdmin(admin.ModelAdmin):
    model           = UnlockPackage
    list_display    = ('name', 'price', 'id')
    search_fields   = ('id','name',)

class PurchaseAdmin(admin.ModelAdmin):
    model = Purchase
    list_display    = ('date', 'id')
    search_fields   = ('id','date', 'user__first__name',
                       'bike__serie_number')

class IslandAdmin(admin.ModelAdmin):
    model = Island
    list_display    = ('name', 'id')
    search_fields   = ('id','name')

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Bike, BikeAdmin)
admin.site.register(UnlockPackage, UnlockPackageAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Island, IslandAdmin)
