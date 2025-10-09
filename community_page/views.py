from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Post
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.contrib import messages

def index(request):
    # Order posts by number of likes (descending), then by creation date
    posts = Post.objects.annotate(
        like_count=Count('likes')
    ).order_by('-like_count', '-created_at')
    
    comment_form = CommentForm()
    return render(request, 'community_page/index.html', {
        'posts': posts,
        'comment_form': comment_form
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('community_home')
    else:
        form = PostForm()
    return render(request, 'community_page/create_post.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({
        "liked": liked,
        "total_likes": post.total_likes(),
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('community_home')

# this is for deleting posts
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only author can delete
    if post.author != request.user:
        messages.error(request, "You don’t have permission to delete this post.")
        return redirect('community')

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return JsonResponse({'deleted': True})

    return JsonResponse({'deleted': False})