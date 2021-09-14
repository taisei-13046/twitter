from django.views.generic import TemplateView, CreateView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login
from django.urls import reverse_lazy

from .forms import SignUpForm


class HomeView(TemplateView):
	template_name = "user/home.html"


class LoginView(TemplateView):
	template_name = "user/login.html"


class LogoutView(TemplateView):
	template_name = "user/logout.html"


class SignUpView(CreateView):
	form_class = SignUpForm
	template_name = "user/index.html"
	success_url = reverse_lazy('user:home')

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		self.object = user
		return HttpResponseRedirect(self.get_success_url())
