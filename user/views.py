from django.views.generic import CreateView, ListView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound

from .forms import SignUpForm
from .models import Follow


class SignUpView(CreateView):
	form_class = SignUpForm
	template_name = "user/index.html"
	success_url = reverse_lazy('blog:home')

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		self.object = user
		return HttpResponseRedirect(self.get_success_url())


class FollowView(ListView):
	model = Follow
	template_name = 'user/follow_home.html'
	success_url = reverse_lazy('blog:home')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		login_user = self.request.user
		target_user = get_object_or_404(User, username=self.kwargs['username'])
		can_follow = Follow.objects.filter(follow_to=target_user, follow_from=login_user).count() == 0
		same_user = login_user == target_user
		context['target_user'] = target_user
		context['can_follow'] = can_follow
		context['same_user'] = same_user
		return context


class FollowCreateView(ListView):
	model = Follow
	template_name = 'user/follow.html'
	success_url = reverse_lazy('blog:home')

	def post(self, request, **kwargs):
		user = get_object_or_404(User, username=self.kwargs['username'])
		if request.user == user:
			return HttpResponseNotFound('<h1>自分自身をフォローすることはできません</h1>')
		if request.user.id is not None:
			follow_relation = Follow.objects.filter(follow_to=user, follow_from=request.user)
			new_follow = Follow(follow_to=user, follow_from=request.user)
			if follow_relation.count() == 0:
				new_follow.save()
		return self.get(self, request, **kwargs)


class FollowDeleteView(ListView):
	model = Follow
	template_name = 'user/unfollow.html'
	success_url = reverse_lazy('blog:home')

	def post(self, request, **kwargs):
		user = get_object_or_404(User, username=self.kwargs['username'])
		if request.user == user:
			return HttpResponseNotFound('<h1>自分自身をフォローすることはできません</h1>')
		if request.user.id is not None:
			follow_relation = Follow.objects.filter(follow_to=user, follow_from=request.user)
			if follow_relation.count() == 1:
				follow_relation.delete()
		return self.get(self, request, **kwargs)
