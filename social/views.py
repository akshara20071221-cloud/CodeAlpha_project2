from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Profile, Post, Comment


# ---------------- HOME ----------------

@login_required
def home(request):

    if request.method == "POST":

        caption = request.POST.get("caption")
        image = request.FILES.get("image")

        Post.objects.create(
            user=request.user,
            caption=caption,
            image=image
        )

        return redirect("home")

    posts = Post.objects.all().order_by("-created_at")

    context = {
        "posts": posts,
    }

    return render(request, "index.html", context)


# ---------------- REGISTER ----------------

def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already exists."
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(user=user)

        return redirect("login")

    return render(request, "register.html")


# ---------------- LOGIN ----------------

def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "login.html")


# ---------------- LOGOUT ----------------

def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- PROFILE ----------------

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        profile.bio = request.POST.get("bio")

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES["profile_image"]

        profile.save()

        return redirect("profile")

    posts = Post.objects.filter(user=request.user).order_by("-created_at")

    context = {
        "profile": profile,
        "posts": posts,
    }

    return render(request, "profile.html", context)


# ---------------- LIKE POST ----------------

@login_required
def like_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("home")


# ---------------- COMMENT ----------------

@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":

        text = request.POST.get("text")

        if text.strip():

            Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )

    return redirect("home")