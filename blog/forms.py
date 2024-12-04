from django import forms
from .models import Post

# Create a form for user to create new post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']