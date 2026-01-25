from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import EditProfileForm
from .models import Follow

User = get_user_model()

def register_view(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            error_message = "Ten nick jest już zajęty"
        elif User.objects.filter(email=email).exists():
            error_message = "Ten email jest już zajęty"
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
def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    posts = profile_user.posts.all().order_by('-created_at')

    is_owner = request.user == profile_user

    is_following = False
    if request.user != profile_user:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    return render(request, 'accounts/profile.html', {'profile_user': profile_user, 'posts': posts, 
                                                     'is_owner': is_owner, 'is_following': is_following,})

@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })



@login_required
def update_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        request.user.avatar = request.FILES['avatar']
        request.user.save()
    return redirect('edit_profile')


@login_required
def remove_avatar(request):
    if request.user.avatar:
        request.user.avatar.delete(save=False)
        request.user.avatar = None
        request.user.save()
    return redirect('edit_profile')

@login_required
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)

    if target != request.user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target
        )

        if not created:
            follow.delete()

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')

    if next_url:
        return redirect(next_url)

    return redirect('user_profile', username=username)



@login_required
def user_list_view(request, username, list_type):
    user = get_object_or_404(User, username=username)

    if list_type == 'followers':
        qs = user.followers.select_related('follower')
        users = [f.follower for f in qs]

        title = "Obserwujący"

    elif list_type == 'following':
        qs = user.following.select_related('following')
        users = [f.following for f in qs]

        title = "Obserwowani"

    else:
        return redirect('profile')

    users = [u for u in users if u != request.user]

    following_ids = set(
        Follow.objects.filter(
            follower=request.user,
            following__in=users
        ).values_list('following_id', flat=True)
    )

    return render(request, 'accounts/user_list.html', {
        'title': title,
        'users': users,
        'following_ids': following_ids,
    })


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('login')

    return redirect('edit_profile')