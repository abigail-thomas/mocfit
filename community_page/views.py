from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Post
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.contrib import messages
from .models import Comment
from django.views.decorators.http import require_POST

def index(request):
    # Get sort parameter from URL, default to 'recent'
    sort_by = request.GET.get('sort', 'recent')
    
    # Base queryset with like count annotation
    posts = Post.objects.annotate(like_count=Count('likes'))
    
    # Apply sorting based on parameter
    if sort_by == 'oldest':
        posts = posts.order_by('created_at')
    elif sort_by == 'likes':
        posts = posts.order_by('-like_count', '-created_at')
    else:  # 'recent' is default
        posts = posts.order_by('-created_at')
    
    comment_form = CommentForm()
    return render(request, 'community_page/index.html', {
        'posts': posts,
        'comment_form': comment_form,
        'current_sort': sort_by
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
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'author': comment.author.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%m/%d/%Y at %I:%M %p'),
                'is_author': True  # Since the person who just posted is always the author
            }
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid form data'
    }, status=400)

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
# this is for the delete comment butto
@login_required
@require_POST
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        
        # Check if the user is the author of the comment
        if comment.author == request.user:
            comment.delete()
            return JsonResponse({'deleted': True})
        else:
            return JsonResponse({'deleted': False, 'error': 'Unauthorized'}, status=403)
    except Comment.DoesNotExist:
        return JsonResponse({'deleted': False, 'error': 'Comment not found'}, status=404)