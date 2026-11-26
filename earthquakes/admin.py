from django.contrib import admin
from .models import Earthquake


@admin.register(Earthquake)
class EarthquakeAdmin(admin.ModelAdmin):
    list_display = ("time", "magnitude", "place", "depth_km")
    list_filter = ("magnitude",)
    search_fields = ("place",)
