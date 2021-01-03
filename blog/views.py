from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Photo
from .forms import PostForm



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

def create(request):
    if(request.method == 'POST'):
        post = Post()
        Post.title = request.POST['title']
        post.text = request.POST['text']
        post.created_date = timezone.now()
        post.author = request.author
        post.save()

        for img in request.FILES.getlist('imgs'):
            photo = Photo()
            photo.post = post
            photo.image = img
            photo.save()
        return  redirect('/detail/' + str(post.id))
    else:
        return render(request, 'new.html')