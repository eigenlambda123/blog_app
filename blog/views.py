from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import PostForm, CustomUserCreation
from .models import Post
from django import forms



# Get add post view
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)  # Basically get the Post form
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'blog/add_post.html', {'form':form})

# Get All Post
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})

# Get Specific Post
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# Edit post
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk) # Prepopulate the form with the existing post data
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
        
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form':form})

# Delete post
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk) # get post
    post.delete() # Delete the post from the database
    return redirect('home')

# create register
def register(request):
    if request.method == 'POST':
        form = CustomUserCreation({
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),   
            'password1': request.POST.get('password1'),
            'password2': request.POST.get('password2'),
        })
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreation()
    return render(request, 'blog/register.html', {'form': form})


# login
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password =  request.POST.get('password')


        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password"
            return render(request, 'blog/login.html', {'error_message': error_message})
    else:
        return render(request, 'blog/login.html')

# logout
def custom_logout(request):
    logout(request)  # This logs out the user
    return redirect('home')  # Redirects to home page after logout