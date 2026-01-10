from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment

# Stary
@login_required
def add_post(request):
    if request.method == 'POST' and request.FILES.get('image'):
        Post.objects.create(
            user=request.user,
            image=request.FILES['image'],
            description=request.POST.get('description', '')
        )
    return redirect('profile')

# Nowy
@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    previous_post = Post.objects.filter(
        author=post.author,
        created_at__lt=post.created_at
    ).first()

    next_post = Post.objects.filter(
        author=post.author,
        created_at__gt=post.created_at
    ).last()

    is_liked = Like.objects.filter(
        user=request.user,
        post=post
    ).exists()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'is_liked': is_liked
    })


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

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

    return redirect(post.get_absolute_url())