from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    profile_user = request.user
    posts = profile_user.posts.all().order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'posts': posts
    })
