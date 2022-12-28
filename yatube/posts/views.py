from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Group, Post, User
from .forms import PostForm


POSTS_PER_PAGE = 10


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template = "posts/index.html"
    context = {"page_obj": page_obj}
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template = "posts/group_list.html"
    context = {"group": group, "page_obj": page_obj}
    return render(request, template, context)


def profile(request, username):
    author = User.objects.get(username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template = "posts/profile.html"
    context = {"page_obj": page_obj, "username": author}
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    posts_count = author.posts.count()
    template = "posts/post_detail.html"
    context = {
        "post": post,
        "posts_count": posts_count,
        "user": request.user.id,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:profile", username=post.author)
        template = "posts/create_post.html"
        context = {"form": form}
        return render(request, template, context)
    form = PostForm()
    template = "posts/create_post.html"
    context = {"form": form}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author_id != request.user.id:
        return redirect("posts:post_detail", post_id=post.pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.author_id = request.user
            post.save()
            return redirect("posts:post_detail", post_id=post.pk)
        template = "posts/create_post.html"
        context = {"form": form}
        return render(request, template, context)
    form = PostForm(instance=post)
    template = "posts/create_post.html"
    context = {"form": form, "is_edit": 1, "post": post}
    return render(request, template, context)
