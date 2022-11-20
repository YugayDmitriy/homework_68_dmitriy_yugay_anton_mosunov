from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DetailView
from django.db.models import Q
from resumes.models import Resume
from vacancies.models.vacancies import Vacancy
from vacancies.forms import VacancyForm, SearchForm

from vacancies.models import VacancyResponse

from vacancies.forms import VacancyResponseForm


class VacanciesIndexView(ListView):
    template_name = 'index_vacancy.html'
    model = Vacancy
    context_object_name = 'vacancies'

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
        queryset = super().get_queryset().exclude(is_deleted=True)
        if self.search_value:
            queryset = Vacancy.objects.filter(title__icontains=self.search_value)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacanciesIndexView, self).get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        return context


class ResumesIndexView(ListView):
    template_name = 'index_resumes.html'
    model = Resume
    context_object_name = 'resumes'

    def get(self, request, *args, **kwargs):
        self.form = SearchForm(self.request.GET)
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')
        return None

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True).exclude(is_public=False).order_by('-created_at')
        if self.search_value:
            queryset = Resume.objects.filter(Q(job_title__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResumesIndexView, self).get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        return context


class VacancyCreateView(CreateView):
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
        return reverse('index')


class VacancyEditView(UpdateView):
    template_name = 'vacancy_edit.html'
    form_class = VacancyForm
    model = Vacancy
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super(VacancyEditView, self).get_context_data(**kwargs)
        context['form'] = VacancyForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse('vacancy_detail', kwargs={'pk': self.object.pk})


class VacancyDetailView(DetailView):
    template_name = 'vacancy_detail.html'
    model = Vacancy
    context_object_name = 'vacancy'

    def get_context_data(self,  **kwargs):
        context = super(VacancyDetailView, self).get_context_data(**kwargs)
        resumes = Resume.objects.exclude(is_deleted=True).exclude(is_public=False)
        context['resumes'] = resumes
        context['vacancy_response_form'] = VacancyResponseForm(current_user=self.request.user)
        return context


class VacancyAddResponseView(CreateView):
    model = VacancyResponse

    def post(self, request, *args, **kwargs):
        hello_message = request.POST['hello_message']
        vacancy = Vacancy.objects.get(pk=kwargs['pk'])
        author = request.user
        resume = request.POST['resume']
        VacancyResponse.objects.create(resume_id=resume, author=author, hello_message=hello_message, vacancy=vacancy)
        return HttpResponse('success')


