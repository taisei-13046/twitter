from django.views.generic import CreateView, ListView
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

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


class FollowingListView(LoginRequiredMixin, ListView):
	model = Follow
	template_name = 'follow/following.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = get_object_or_404(User, username=self.kwargs['username'])
		context['following_list'] = user.following.all()
		return context


class FollowerListView(LoginRequiredMixin, ListView):
	model = Follow
	template_name = 'follow/follower.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = get_object_or_404(User, username=self.kwargs['username'])
		context['follower_list'] = user.follower.all()
		return context


class FollowIndexView(LoginRequiredMixin, ListView):
	model = Follow
	template_name = 'follow/follow_index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		login_user = self.request.user
		target_user = get_object_or_404(User, username=self.kwargs['username'])
		has_followed = Follow.objects.filter(follow_to=target_user, follow_from=login_user).count() != 0
		is_same_user = login_user == target_user
		context['target_user'] = target_user
		context['has_followed'] = has_followed
		context['is_same_user'] = is_same_user
		return context


@login_required
def follow_view(request, *args, **kwargs):
	follower = request.user
	try:
		following = User.objects.get(username=kwargs['username'])
	except User.DoesNotExist:
		raise Http404('this user does not exist.')
	if follower == following:
		raise PermissionDenied()
	follow_relation = Follow.objects.filter(follow_to=following, follow_from=follower)
	if not follow_relation.count():
		new_follow = Follow(follow_to=following, follow_from=follower)
		new_follow.save()
	return HttpResponseRedirect(reverse('blog:home'))


@login_required
def unfollow_view(request, *args, **kwargs):
	follower = request.user
	try:
		following = User.objects.get(username=kwargs['username'])
	except User.DoesNotExist:
		raise Http404('this user does not exist.')
	follow_relation = Follow.objects.filter(follow_to=following, follow_from=follower)
	if follow_relation.count():
		follow_relation.delete()
	return HttpResponseRedirect(reverse('blog:home'))
