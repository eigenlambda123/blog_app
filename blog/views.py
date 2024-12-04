from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post

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