from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DetailView, DeleteView
from django.db.models import Q
from resumes.models import Resume
from vacancies.models.vacancies import Vacancy
from vacancies.forms import VacancyForm, SearchForm
from vacancies.models import VacancyResponse
from vacancies.forms import VacancyResponseForm
from vacancies.forms import VacancyChatForm
from vacancies.models import VacancyChat

from resumes.models import Profession

from vacancies.models import Specialization


class VacanciesIndexView(LoginRequiredMixin, ListView):
    template_name = 'index_vacancy.html'
    model = Vacancy
    context_object_name = 'vacancies'
    paginate_by = 4
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        if self.request.user.user_category == 'employer' or self.request.user == 'root':
            return redirect('index_resumes', pk=self.request.user.pk)
        else:
            self.form = SearchForm(self.request.GET)
            self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')
        return None

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True).exclude(is_public=False).order_by('-changed_at')
        if self.search_value:
            queryset = Vacancy.objects.filter(title__icontains=self.search_value)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacanciesIndexView, self).get_context_data(object_list=object_list, **kwargs)
        context['specializations'] = Specialization.objects.all()
        context['form'] = self.form
        return context


class ResumesIndexView(LoginRequiredMixin, ListView):
    template_name = 'index_resumes.html'
    model = Resume
    context_object_name = 'resumes'
    paginate_by = 4
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = SearchForm(self.request.GET)
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')
        return None

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True).exclude(is_public=False).order_by('-changed_at')
        if self.search_value:
            queryset = Resume.objects.filter(Q(job_title__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResumesIndexView, self).get_context_data(object_list=object_list, **kwargs)
        context['professions'] = Profession.objects.all()
        context['form'] = self.form
        return context


class VacancyCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create_vacancy.html'
    form_class = VacancyForm
    model = Vacancy

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author_id = self.kwargs['pk']
            post = form.save()
            return redirect('profile', pk=self.kwargs['pk'])
        context = {}
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(VacancyCreateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


class VacancyPublicView(TemplateView):
    model = Vacancy

    def post(self, request, *args, **kwargs):
        vacancy = Vacancy.objects.get(id=kwargs['pk'])
        if vacancy.is_public:
            vacancy.is_public = False
            vacancy.save()
            return redirect('profile', pk=request.user.pk)
        if not vacancy.is_public:
            vacancy.is_public = True
            vacancy.save()
        return redirect('profile', pk=request.user.pk)


class VacancyUpdateDateView(TemplateView):
    model = Vacancy

    def post(self, request, *args, **kwargs):
        vacancy = Vacancy.objects.get(id=kwargs['pk'])
        vacancy.changed_at = datetime.now()
        vacancy.save()
        return redirect('profile', pk=request.user.pk)


class VacancyEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'vacancy_edit.html'
    form_class = VacancyForm
    model = Vacancy
    context_object_name = 'vacancy'
    permission_required = 'vacancies.change_resume'

    def has_permission(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        context = super(VacancyEditView, self).get_context_data(**kwargs)
        context['form'] = VacancyForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse('vacancy_detail', kwargs={'pk': self.object.pk})


class VacancyDetailView(LoginRequiredMixin, DetailView):
    template_name = 'vacancy_detail.html'
    model = Vacancy
    context_object_name = 'vacancy'

    def get_context_data(self,  **kwargs):
        context = super(VacancyDetailView, self).get_context_data(**kwargs)
        resumes = Resume.objects.exclude(is_deleted=True).exclude(is_public=False)
        context['resumes'] = resumes
        context['vacancy_response_form'] = VacancyResponseForm(current_user=self.request.user)
        return context


class VacancyAddResponseView(LoginRequiredMixin, CreateView):
    model = VacancyResponse

    def post(self, request, *args, **kwargs):
        hello_message = request.POST['hello_message']
        vacancy = Vacancy.objects.get(pk=kwargs['pk'])
        author = request.user
        resume = request.POST['resume']
        VacancyResponse.objects.create(resume_id=resume, author=author, hello_message=hello_message, vacancy=vacancy)
        return HttpResponse('success')


class ToVacanciesResponsesView(LoginRequiredMixin, ListView):
    template_name = 'vacancies_response.html'
    model = Vacancy
    context_object_name = 'vacancies'

    def get(self, request, *args, **kwargs):
        print(self.template_name)
        self.form = VacancyChatForm()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True).order_by('-created_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ToVacanciesResponsesView, self).get_context_data(object_list=object_list, **kwargs)
        context['vacancy_chat_form'] = self.form
        return context


class VacancyAddChatMessageView(LoginRequiredMixin, CreateView):
    model = VacancyChat
    form_class = VacancyChatForm

    def post(self, request, *args, **kwargs):
        response = VacancyResponse.objects.get(id=kwargs['pk'])
        message = request.POST['message']
        author = self.request.user
        print(author)
        VacancyChat.objects.create(response=response, message=message, author=author)
        return redirect('to_vacancies_responses', pk=self.request.user.pk)


class VacancyDeleteView(DeleteView):
    template_name = 'vacancy_confirm_delete.html'
    model = Vacancy

    def post(self, request, *args, **kwargs):
        vacancy = Vacancy.objects.get(pk=kwargs['pk'])
        vacancy.deleted_at = timezone.now()
        vacancy.is_deleted = True
        vacancy.save()
        return redirect('profile', pk=self.request.user.pk)


def vacancy_category_view(request, category):
    form = SearchForm(request.GET)
    search_value = get_search_value(form)
    specializations = Specialization.objects.all()
    if search_value:
        vacancies = Vacancy.objects.filter(Q(title__icontains=search_value))
        context = {
            'form': SearchForm(),
            'vacancies': vacancies,
            'specializations': specializations
        }
        return render(request, 'index_vacancy.html', context)
    specialization = Specialization.objects.get(specialization_name=category)
    vacancies = Vacancy.objects.filter(specialization=specialization.pk, is_deleted=False).order_by('changed_at')
    context = {
        'form': SearchForm(),
        'vacancies': vacancies,
        'specializations': specializations
    }
    return render(request, 'index_vacancy.html', context)


def get_search_value(form):
    if form.is_valid():
        return form.cleaned_data.get('search')
    return None


def vacancy_salary_sort_view(request, choice):
    form = SearchForm(request.GET)
    search_value = get_search_value(form)
    specializations = Specialization.objects.all()

    if search_value:
        if choice == 1:
            vacancies = Vacancy.objects.filter(Q(title__icontains=search_value)).order_by('salary_level')
        elif choice == 0:
            vacancies = Vacancy.objects.filter(Q(title__icontains=search_value)).order_by('-salary_level')
        context = {
            'form': SearchForm(),
            'vacancies': vacancies,
            'specializations': specializations
        }
        return render(request, 'index_vacancy.html', context)
    if choice == 1:
        vacancies = Vacancy.objects.filter(is_deleted=False).order_by('salary_level')
    elif choice == 0:
        vacancies = Vacancy.objects.filter(is_deleted=False).order_by('-salary_level')
    find_form = SearchForm()
    context = {
        'form': find_form,
        'vacancies': vacancies,
        'specializations': specializations
    }
    return render(request, 'index_vacancy.html', context)

