from django.contrib import admin

from .models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "chat_id", "word")
    list_display_links = ("full_name",)
    ordering = ("id",)

