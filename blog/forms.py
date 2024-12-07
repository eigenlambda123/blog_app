from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create a form for user to create new post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your content here...',
                'rows': 6,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Content',
            'image': 'Post Image',
        }

    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        def __init__(self, *args, **kwargs):
            user = kwargs.get('user', None)
            super().__init__(*args, **kwargs)
            if user and user.is_authenticated:
                self.fields['name'].required = False
                self.fields['email'].required = False


class CustomUserCreation(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'location']