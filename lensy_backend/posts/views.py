from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from .models import Post, Like, Comment, CommentLike, Hashtag
from accounts.models import Follow


@login_required
def add_post(request):
    if request.method == 'POST' and request.FILES.get('image'):
        Post.objects.create(
            author=request.user,
            image=request.FILES['image'],
            description=request.POST.get('description', '')
        )
    return redirect('profile')

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    previous_post = (
        Post.objects.filter(
            author=post.author,
            created_at__lt=post.created_at
        ).order_by('-created_at').first()
    )

    next_post = (
        Post.objects.filter(
            author=post.author,
            created_at__gt=post.created_at
        ).order_by('created_at').first()
    )

    is_liked = Like.objects.filter(
        user=request.user,
        post=post
    ).exists()

    liked_comment_ids = set(
        CommentLike.objects.filter(
            user=request.user,
            comment__post=post
        ).values_list('comment_id', flat=True)
    )

    following_ids = set(
        Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)
    )

    return_to = request.GET.get('from')

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'is_liked': is_liked,
        'liked_comment_ids': liked_comment_ids,
        'following_ids': following_ids,
        'return_to': return_to,
    })



@login_required
def toggle_like_home(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect(request.POST.get('next', '/'))


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return_to = request.POST.get('from')

    if return_to:
        return redirect(f"{post.get_absolute_url()}?from={return_to}")

    return redirect(post.get_absolute_url())


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )

    return_to = request.POST.get('from')

    if return_to:
        return redirect(f"{post.get_absolute_url()}?from={return_to}")

    return redirect(post.get_absolute_url())


@login_required
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    like, created = CommentLike.objects.get_or_create(
        user=request.user,
        comment=comment
    )

    if not created:
        like.delete()

    return_to = request.POST.get('from')

    if return_to:
        return redirect(
            f"{comment.post.get_absolute_url()}?from={return_to}"
        )

    return redirect(comment.post.get_absolute_url())


@login_required
def hashtag_feed_view(request, name):
    hashtag = get_object_or_404(Hashtag, name=name.lower())

    posts_qs = (
        Post.objects
        .filter(hashtags=hashtag)
        .select_related('author')
        .prefetch_related('hashtags', 'likes', 'comments')
        .order_by('-created_at')
    )

    paginator = Paginator(posts_qs, 5) 
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    liked_post_ids = set(
        Like.objects.filter(
            user=request.user,
            post__in=posts
        ).values_list('post_id', flat=True)
    )

    return render(request, 'core/home.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'active_hashtag': hashtag,
    })


@login_required
def delete_comment_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user != request.user:
        return HttpResponseForbidden()

    post_id = comment.post.id

    if request.method == 'POST':
        comment.delete()

    return redirect('post_detail', post_id=post_id)



@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post.delete()
        return redirect('profile')

    return redirect(post.get_absolute_url())