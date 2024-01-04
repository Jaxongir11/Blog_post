from django.db.models import Count
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Category, Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from hitcount.views import HitCountDetailView


class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        queryset = Post.objects.filter(status=1).order_by('-created_on')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['mahalliy'] = Post.objects.filter(category__name='Mahalliy', status=1).order_by('-created_on')[:4]
        context['xorij'] = Post.objects.filter(category__name='Xorij', status=1).order_by('-created_on')[:4]
        context['sport'] = Post.objects.filter(category__name='Sport', status=1).order_by('-created_on')[:4]
        context['siyosat'] = Post.objects.filter(category__name='Siyosat', status=1).order_by('-created_on')[:4]
        context['oxirgi_post'] = Post.objects.filter(status=1).order_by('-created_on')[:3]
        context['kop_korilgan_post'] = Post.objects.filter(status=1).order_by('-hit_count_generic__hits')[:4]
        return context


def popular_posts(request,period):
    if period == 'week':
        start_date = timezone.now() - timezone.timedelta(days=7)
    elif period == 'month':
        start_date = timezone.now() - timezone.timedelta(days=30)
    else:
        start_date = timezone.datetime.min

    posts = Post.objects.filter(status=1, created_on__gte=start_date).order_by('-hit_count_generic__hits')

    context = {
        'period': period,
        'posts': posts,
    }

    return render(request, 'post/popular_posts.html', context)


def last_posts(request):
    posts = Post.objects.filter(status=1).order_by('-created_on')[:10]
    context = {
        'posts': posts,
    }

    return render(request, 'post/last_posts.html', context)


class CategoryArchiveView(View):
    template_name = 'post/category-archive.html'

    def get(self, request, *args, **kwargs):
        category_slug = kwargs.get('category')
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category, status=1).order_by('-created_on')
        # Perform any additional logic based on the category if needed
        context = {
            'category': category,
            'posts': posts,
        }
        return render(request, self.template_name, context)


class PostDetailView(HitCountDetailView, DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post_detail'
    count_hit = True


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'post/post_create.html'
    context_object_name = 'post_create'
    success_url = reverse_lazy('post:post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author
        form.instance.created_on = timezone.now()  # Set the creation time
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_update.html'  # Replace with your desired template
    context_object_name = 'post_update'
    success_url = reverse_lazy('post:post-list')  # Replace with your desired success URL

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'  # Replace with your desired template
    context_object_name = 'post_delete'
    success_url = reverse_lazy('post:post-list')


@login_required
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    return redirect('post:post-detail', slug=slug)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/comment_update.html'  # Replace with your desired template
    context_object_name = 'comment_update'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author
        return super().form_valid(form)

    def get_success_url(self):
        post_slug = self.object.post.slug
        # Check if the associated post has a non-empty slug
        if post_slug:
            return reverse('post:post-detail', kwargs={'slug': post_slug})
        else:
            # Handle the case where the slug is empty (adjust this according to your logic)
            return reverse('post:post-list')  # Redirect to post-list as an example

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'post/comment_confirm_delete.html'  # Replace with your desired template
    context_object_name = 'comment_delete'
    success_url = reverse_lazy('post:post-detail')

    def get_success_url(self):
        post_slug = self.object.post.slug
        # Check if the associated post has a non-empty slug
        if post_slug:
            return reverse('post:post-detail', kwargs={'slug': post_slug})
        else:
            # Handle the case where the slug is empty (adjust this according to your logic)
            return reverse('post:post-list')

