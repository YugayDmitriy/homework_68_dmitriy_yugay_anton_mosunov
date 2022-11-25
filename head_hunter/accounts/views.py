from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from accounts.forms import LoginForm, CustomUserCreationForm, UserChangeForm, PasswordChangeForm
from resumes.models import Resume
from vacancies.models.vacancies import Vacancy


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
        print('sdfgdsbdfndfngdhgdhj')
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            print('111111111111111')
            account = form.save()
            login(request, account)
            return redirect('profile', pk=account.pk)
        context = {}
        context['form'] = form
        return self.render_to_response(context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.object
        resumes = Resume.objects.filter(author=account).exclude(is_deleted=True)
        vacancies = Vacancy.objects.filter(author=account).exclude(is_deleted=True)
        context['resumes'] = resumes
        context['vacancies'] = vacancies
        return context


class UserChangeView(PermissionRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'
    permission_required = 'accounts.change_account'

    def has_permission(self):
        return self.get_object().username == self.request.user.username

    def get_context_data(self, **kwargs):
        context = super(UserChangeView, self).get_context_data(**kwargs)
        context['form'] = UserChangeForm(instance=self.object)
        return context

    def get_profile_form(self):
        form_kwargs = {'instance': self.object}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
        return UserChangeForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super(UserChangeView, self).form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


class UserPasswordChangeView(PermissionRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'
    permission_required = 'accounts.change_account'

    def has_permission(self):
        return self.get_object().username == self.request.user.username
    def get_success_url(self):
        return reverse('login')
