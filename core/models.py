from django.conf import settings
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = [("patient", "Patient"), ("doctor", "Doctor")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default="patient")
    bio = models.TextField(blank=True)
    qualification = models.CharField(max_length=160, blank=True)
    is_verified = models.BooleanField(default=False, help_text="Admin verifies credentials before doctor can chat.")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Product(models.Model):
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="patient_messages", on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="doctor_messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_chat_messages", on_delete=models.CASCADE)
    body = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created_at"]
    def __str__(self):
        return f"{self.sender.username}: {self.body[:40]}"
