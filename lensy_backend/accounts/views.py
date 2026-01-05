from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm

User = get_user_model()

def register_view(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            error_message = "Użytkownik z tym email lub nazwą użytkownika już istnieje"
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            success_message = "Konto zostało utworzone"
            return redirect("login")

    return render(request, "accounts/register.html", {
        "error_message": error_message,
        "success_message": success_message
    })


def login_view(request):
    error_message = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error_message = "Niepoprawne dane logowania"

    return render(request, "accounts/login.html", {"error_message": error_message})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    user = request.user
    return render(request, "accounts/profile.html", {"profile_user": user})


@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })
