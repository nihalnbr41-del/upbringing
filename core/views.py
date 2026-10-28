from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import RegisterForm, ChatMessageForm
from .models import Profile, Product, ChatMessage

def home(request):
    featured = Product.objects.filter(is_available=True)[:3]
    return render(request, "core/index.html", {"featured": featured})

def about(request):
    return render(request, "core/about.html")

def resources(request):
    return render(request, "core/resources.html")

def shop(request):
    category = request.GET.get("category", "")
    products = Product.objects.filter(is_available=True)
    if category:
        products = products.filter(category__iexact=category)
    categories = Product.objects.filter(is_available=True).values_list("category", flat=True).distinct()
    return render(request, "core/shop.html", {"products": products, "categories": categories, "selected": category})

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        messages.success(request, "Account created. You can now sign in.")
        return redirect("login")
    return render(request, "core/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username", ""), password=request.POST.get("password", ""))
        if user:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Username or password was not recognised.")
    return render(request, "core/login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect("admin_dashboard")
    profile = getattr(request.user, "profile", None)
    if not profile:
        profile = Profile.objects.create(user=request.user)
    if profile.role == "doctor":
        chats = ChatMessage.objects.filter(doctor=request.user).values("patient_id", "patient__username").distinct()
        return render(request, "core/doctor_dashboard.html", {"profile": profile, "chats": chats})
    doctors = Profile.objects.filter(role="doctor", is_verified=True).select_related("user")
    return render(request, "core/patient_dashboard.html", {"profile": profile, "doctors": doctors})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Admin access only.")
    profiles = Profile.objects.select_related("user").order_by("-created_at")
    if request.method == "POST":
        profile_id = request.POST.get("profile_id")
        profile = get_object_or_404(Profile, id=profile_id, role="doctor")
        profile.is_verified = request.POST.get("action") == "verify"
        profile.save(update_fields=["is_verified"])
        messages.success(request, f"Doctor status updated for {profile.user.username}.")
        return redirect("admin_dashboard")
    return render(request, "core/admin_dashboard.html", {
        "profiles": profiles, "patient_count": Profile.objects.filter(role="patient").count(),
        "doctor_count": Profile.objects.filter(role="doctor").count(),
        "product_count": Product.objects.count(), "message_count": ChatMessage.objects.count(),
    })

@login_required
def chat(request):
    profile = getattr(request.user, "profile", None)
    if not profile:
        return redirect("dashboard")
    if profile.role == "doctor":
        if not profile.is_verified:
            messages.warning(request, "Your doctor profile must be verified by an admin before chatting.")
            return redirect("dashboard")
        patient_id = request.GET.get("patient")
        patient = get_object_or_404(User, id=patient_id, profile__role="patient")
        doctor, patient_user = request.user, patient
    else:
        doctor_id = request.GET.get("doctor")
        doctor_profile = get_object_or_404(Profile, id=doctor_id, role="doctor", is_verified=True)
        doctor, patient_user = doctor_profile.user, request.user

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            ChatMessage.objects.create(patient=patient_user, doctor=doctor, sender=request.user,
                                       body=form.cleaned_data["body"])
            return redirect(request.get_full_path())
    else:
        form = ChatMessageForm()
    messages_list = ChatMessage.objects.filter(patient=patient_user, doctor=doctor).select_related("sender")
    return render(request, "core/chat.html", {
        "form": form, "messages_list": messages_list, "doctor": doctor,
        "patient": patient_user, "is_doctor": profile.role == "doctor",
    })
