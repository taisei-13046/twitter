from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import PostCreateForm, PostUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404, JsonResponse


from .models import Post, Like
from user.models import Follow


class HomeView(LoginRequiredMixin, ListView):
    model = User
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_user = self.request.user
        context['following_count'] = Follow.objects.filter(follow_from=login_user).count()
        context['follower_count'] = Follow.objects.filter(follow_to=login_user).count()
        context['post_list'] = Post.objects.all()
        return context


class CreateTweetView(LoginRequiredMixin, CreateView):
    """作成"""
    form_class = PostCreateForm
    template_name = "blog/create_tweet.html"
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DetailTweetView(LoginRequiredMixin, DetailView):
    """詳細"""
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


class UpdateTweetView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """更新"""
    model = Post
    template_name = 'blog/update.html'
    form_class = PostUpdateForm
    success_url = reverse_lazy('blog:home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class DeleteTweetView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """削除"""
    model = Post
    success_url = reverse_lazy('blog:home')
    template_name = 'blog/delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


@login_required
@require_POST
def like_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404('this post does not exist')
    like = Like.objects.filter(post=post, user=request.user)
    if not like:
        Like.objects.create(post=post, user=request.user)
    context = {
        'liked': True,
        'count': post.like__set.count()
    }
    if request.is_ajax():
        return JsonResponse(context)


@login_required
@require_POST
def unlike_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404('this post does not exist')
    like = Like.objects.filter(post=post, user=request.user)
    if like:
        like.delete()
    context = {
        'liked': False,
        'count': post.like__set.count()
    }
    if request.is_ajax():
        return JsonResponse(context)
