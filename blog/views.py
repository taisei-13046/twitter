from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import PostCreateForm, PostUpdateForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Post, Follow


class HomeView(LoginRequiredMixin, ListView):
    model = User
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all()
        context['post_list'] = post_list
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


class FollowingListView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = 'blog/following.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        following_list = user.following.values_list("follow_to")
        context['following_list'] = User.objects.filter(id__in=following_list)
        return context


class FollowerListView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = 'blog/follower.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        follower_list = user.follower.values_list("follow_from")
        context['follower_list'] = User.objects.filter(id__in=follower_list)
        return context


class FollowAllowView(ListView):
    model = Follow
    template_name = 'blog/follow_allow.html'
    success_url = reverse_lazy('blog:home')

    def get_context_data(self, **kwargs):
        context = super(FollowAllowView, self).get_context_data(**kwargs)
        login_user = self.request.user
        target_user = get_object_or_404(User, username=self.kwargs['username'])
        can_follow = Follow.objects.filter(follow_to=target_user, follow_from=login_user).count() == 0
        same_user = login_user == target_user
        context['target_user'] = target_user
        context['can_follow'] = can_follow
        context['same_user'] = same_user
        return context

    def post(self, request, **kwargs):
        if request.user.id is not None:
            user = get_object_or_404(User, username=self.kwargs['username'])
            follow_relation = Follow.objects.filter(follow_to=user, follow_from=request.user)
            if 'follow' in request.POST:
                new_follow = Follow(follow_to=user, follow_from=request.user)
                if follow_relation.count() == 0:
                    new_follow.save()
            elif 'unfollow' in request.POST:
                if follow_relation.count() == 1:
                    follow_relation.delete()
        return self.get(self, request, **kwargs)
