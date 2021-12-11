from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post

class PostListView(ListView):
    model = Post

def post_detail(request, slug=None):
    if slug is None:
        try:
            post = Post.objects.filter(created_on__isnull=False).latest('created_on')
        except Post.DoesNotExist:
            raise Http404("Post does not exist")
    else:
        post = get_object_or_404(Post, slug=slug)

    try:
        next_post = post.get_next_by_created_on()
    except Post.DoesNotExist:
        next_post = None

    try:
        previous_post = post.get_previous_by_created_on()
    except Post.DoesNotExist:
        previous_post = None

    return render(request, 'blog/index.html', {
        'post': post,
        'next_post': next_post,
        'previous_post': previous_post
    })


def about(request):
    return render(request, 'blog/about.html')
