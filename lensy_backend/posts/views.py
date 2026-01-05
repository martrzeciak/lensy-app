from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
def add_post(request):
    if request.method == 'POST' and request.FILES.get('image'):
        Post.objects.create(
            user=request.user,
            image=request.FILES['image'],
            description=request.POST.get('description', '')
        )
    return redirect('profile')