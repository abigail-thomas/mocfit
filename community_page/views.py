from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Post
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.contrib import messages
from .models import Comment
from django.views.decorators.http import require_POST
import json

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
    # the post request method
    if request.method == 'POST':
        # the post form
        form = PostForm(request.POST, request.FILES)
        # the form is valid
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('community_home')
    # the get request method
    else:
        # the post form
        form = PostForm()
    return render(request, 'community_page/create_post.html', {'form': form})

@login_required
def like_post(request, post_id):
    # the post object
    post = get_object_or_404(Post, id=post_id)
    # the user is in the post likes
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        # the user is not in the post likes
        post.likes.add(request.user)
        liked = True
    # the json response
    return JsonResponse({
        "liked": liked,
        "total_likes": post.total_likes(),
    })

@login_required
@require_POST
def add_comment(request, post_id):
    # the post object
    post = get_object_or_404(Post, id=post_id)
    # the comment form
    form = CommentForm(request.POST)
    
    # check if the form is valid
    if form.is_valid():
        # create a new comment
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

        # return the comment in a json response
        return JsonResponse({
            'success': True,
            'comment': {
                # the comment id    
                'id': comment.id,
                # the comment author
                'author': comment.author.username,
                # the comment content
                'content': comment.content,
                # the comment created at
                'created_at': comment.created_at.strftime('%m/%d/%Y'),
                'is_author': True # Since the person who just posted is always the author
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


@login_required
@require_POST
def post_workout_to_community(request):
    """Post a generated workout to the community feed"""
    try:
        description = request.POST.get('description', '')
        
        # Get workout data from session
        workout_data = request.session.get('current_workout', {})
        
        if not workout_data:
            return JsonResponse({'success': False, 'error': 'No workout data found'}, status=400)
        
        # Format the workout content for the post
        workout_type = workout_data.get('workout_type', 'preset')
        category = workout_data.get('category', '')
        goal = workout_data.get('goal', '')
        total_exercises = workout_data.get('total_exercises', 0)
        estimated_duration = workout_data.get('estimated_duration', '')
        
        # Build the workout summary content
        workout_summary = f"🏋️ Workout: {category}\n"
        workout_summary += f"🎯 Goal: {goal}\n"
        workout_summary += f"💪 Exercises: {total_exercises}\n"
        workout_summary += f"⏱️ Duration: {estimated_duration}\n\n"
        
        # Add exercises list
        if workout_type == 'preset':
            exercises = workout_data.get('exercises', [])
            if exercises:
                workout_summary += "📋 Exercises:\n"
                for i, ex in enumerate(exercises[:10], 1):  # Limit to first 10
                    workout_summary += f"  {i}. {ex.get('name', '')}\n"
                if len(exercises) > 10:
                    workout_summary += f"  ... and {len(exercises) - 10} more\n"
        elif workout_type == 'advanced':
            workout = workout_data.get('workout', {})
            workout_summary += "📋 Exercises:\n"
            count = 0
            for muscle_name, exercise_list in workout.items():
                for entry in exercise_list:
                    count += 1
                    if count <= 10:
                        ex_name = entry.get('exercise', {}).get('name', '')
                        sets = entry.get('sets', '')
                        reps = entry.get('reps', '')
                        workout_summary += f"  {count}. {ex_name} ({sets}x{reps})\n"
            if count > 10:
                workout_summary += f"  ... and {count - 10} more\n"
        
        # Add user description if provided
        if description:
            workout_summary += f"\n📝 {description}"
        
        # Create the post
        post = Post.objects.create(
            author=request.user,
            content=workout_summary
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Workout posted to community!',
            'redirect_url': '/community/'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)