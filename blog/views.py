from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, View, DetailView, DeleteView, UpdateView
from .forms import PostCreateForm, PostUpdateForm
from django.urls import reverse_lazy
from django.shortcuts import render

from .models import Post


class HomeView(LoginRequiredMixin, View):

    def get(self, request):
        post_list = Post.objects.all()
        context = {
            'post_list': post_list,
        }
        return render(request, 'blog/home.html', context)


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
