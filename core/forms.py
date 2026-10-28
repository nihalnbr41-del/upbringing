from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ChatMessage

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    qualification = forms.CharField(required=False, help_text="Doctors: enter your qualification for admin verification.")
    class Meta:
        model = User
        fields = ("username", "email", "role", "qualification", "password1", "password2")
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(user=user, role=self.cleaned_data["role"],
                                   qualification=self.cleaned_data.get("qualification", ""))
        return user

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ("body",)
        widgets = {"body": forms.TextInput(attrs={"placeholder": "Write a supportive message…", "maxlength": 2000})}
