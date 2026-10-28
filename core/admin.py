from django.contrib import admin
from .models import Profile, Product, ChatMessage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "qualification", "is_verified", "created_at")
    list_filter = ("role", "is_verified")
    search_fields = ("user__username", "user__email", "qualification")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "sender", "created_at")
    readonly_fields = ("patient", "doctor", "sender", "body", "created_at")
