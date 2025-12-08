from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # the post author
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    # the post content
    content = models.TextField(blank=True)
    # the post image
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    # the post created at
    created_at = models.DateTimeField(auto_now_add=True)
    # the post likes
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    # the total likes
    def total_likes(self):
        return self.likes.count()

    # the post string representation
    def __str__(self):
        return f"{self.author.username}'s post on {self.created_at.strftime('%Y-%m-%d')}"

class Comment(models.Model):
    # the comment post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # the comment author
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # the comment content
    content = models.TextField()
    # the comment created at
    created_at = models.DateTimeField(auto_now_add=True)

    # the comment string representation
    def __str__(self):
        return f"Comment by {self.author.username}"
