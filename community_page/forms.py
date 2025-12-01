from django import forms
from django.core.exceptions import ValidationError
from PIL import Image
from .models import Post, Comment

# Maximum file size: 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes

# Allowed image formats
ALLOWED_FORMATS = ['JPEG', 'JPG', 'PNG', 'WEBP']

# Maximum dimensions (will be resized if larger)
MAX_WIDTH = 1080
MAX_HEIGHT = 1350  # Instagram's max aspect ratio is 4:5 (1080x1350)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Share your fitness journey...',
                'rows': 4,
            }),
            'image': forms.FileInput(attrs={
                'accept': 'image/jpeg,image/png,image/webp',
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            # Check file size
            if image.size > MAX_FILE_SIZE:
                raise ValidationError(
                    f'Image file too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB. '
                    f'Your file is {image.size / (1024*1024):.1f}MB.'
                )
            
            # Validate it's actually an image and check format
            try:
                img = Image.open(image)
                img.verify()  # Verify it's a valid image
                
                # Reopen after verify (verify closes the file)
                image.seek(0)
                img = Image.open(image)
                
                # Check format
                if img.format.upper() not in ALLOWED_FORMATS:
                    raise ValidationError(
                        f'Unsupported image format: {img.format}. '
                        f'Please use JPEG, PNG, or WebP.'
                    )
                
                # Check minimum dimensions (too small looks bad)
                width, height = img.size
                if width < 320 or height < 320:
                    raise ValidationError(
                        f'Image too small ({width}x{height}). '
                        f'Minimum size is 320x320 pixels.'
                    )
                
                # Reset file pointer for saving
                image.seek(0)
                
            except Exception as e:
                if isinstance(e, ValidationError):
                    raise
                raise ValidationError(
                    'Invalid image file. Please upload a valid JPEG, PNG, or WebP image.'
                )
        
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write a comment...',
                'rows': 2,
            }),
        }
