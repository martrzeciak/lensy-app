from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from posts.models import Post
from accounts.models import Follow


@login_required
def home_view(request):
    following_ids = set(
        Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)
    )

    posts = Post.objects.filter(
        author_id__in=following_ids
    ).select_related('author').order_by('-created_at')

    return render(request, 'core/home.html', {'posts': posts})

