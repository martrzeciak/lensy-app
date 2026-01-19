from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from posts.models import Post, Like, Comment
from accounts.models import Follow


@login_required
def home_view(request):
    following_ids = set(
        Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)
    )

    posts = (
        Post.objects.filter(author_id__in=following_ids)
        .select_related('author')
        .prefetch_related('likes', 'comments')
        .order_by('-created_at')
    )

    liked_post_ids = set(
        Like.objects.filter(
            user=request.user,
            post__in=posts
        ).values_list('post_id', flat=True)
    )

    return render(request, 'core/home.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
    })

