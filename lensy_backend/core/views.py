from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from posts.models import Post, Like, Hashtag
from accounts.models import Follow

User = get_user_model()


@login_required
def home_view(request):
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('following_id', flat=True)

    posts = (
        Post.objects
        .filter(author__in=list(following_ids) + [request.user.id])
        .select_related('author')
        .prefetch_related('hashtags', 'likes', 'comments')
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



@login_required
def search_view(request):
    q = request.GET.get('q', '').strip()

    if not q:
        return redirect('home')

    # HASHTAG
    if q.startswith('#'):
        tag_name = q[1:].lower()
        try:
            hashtag = Hashtag.objects.get(name=tag_name)
            return redirect('hashtag_feed', name=hashtag.name)
        except Hashtag.DoesNotExist:
            return redirect('home')

    # USERNAME
    try:
        user = User.objects.get(username__iexact=q)
        return redirect('user_profile', username=user.username)
    except User.DoesNotExist:
        return redirect('home')