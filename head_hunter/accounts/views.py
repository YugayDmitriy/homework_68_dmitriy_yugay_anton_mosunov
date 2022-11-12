from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from accounts.forms import LoginForm
from django.core.paginator import Paginator

from accounts.forms import CustomUserCreationForm

# from accounts.forms import UserChangeForm
# from posts.models import Post
# from accounts.models import Account
# from accounts.forms import PasswordChangeForm
# from accounts.forms import SearchForm


# from accounts.forms import ProfileChangeForm


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        next = request.GET.get('next')
        form_data = {} if not next else {'next': next}
        form = self.form(form_data)
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect('login')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        next = form.cleaned_data.get('next')
        account = authenticate(request, email=email, password=password)
        if not account:
            return redirect('login')
        login(request, account)
        if next:
            return redirect(next)
        return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('login')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    # success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            account = form.save()
            login(request, account)
            return redirect('profile', pk=account.pk)
        context = {}
        context['form'] = form
        return self.render_to_response(context)