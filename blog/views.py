from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import PostForm, CustomUserCreation, UserUpdateForm, ProfileUpdateForm, CommentForm
from .models import Post
from django import forms
from django.views.generic import DeleteView, CreateView 
from django.urls import reverse_lazy



#Profile
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('home')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile.html', context)


# Get add post view
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Basically get the Post form
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'blog/add_post.html', {'form':form})

# Get All Post
def home(request):
    posts = Post.objects.prefetch_related('comments').order_by('-created_at')  # Order by latest
    return render(request, 'blog/home.html', {'posts': posts})


# Get Specific Post
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Ensure post exists
    comments = post.comments.all()

    # Handle comment form submission
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.name = request.user.username  # Set name as the username
                comment.email = request.user.email
                comment.author = request.user  # Associate logged-in user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    # Pass the necessary context
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })



# Edit post
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form})


# Delete post
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return HttpResponseForbidden("You are not allowed to delete this post.")
        return super().dispatch(request, *args, **kwargs)
    
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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


# Ordering Edit
def home(request):
    posts = Post.objects.all().order_by('-created_at')  # Order by 'created_at' descending
    return render(request, 'blog/home.html', {'posts': posts})