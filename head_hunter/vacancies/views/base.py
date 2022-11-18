from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.db.models import Q
from urllib.parse import urlencode

from resumes.models import Resume
from vacancies.models.vacancies import Vacancy
from vacancies.forms import VacancyForm, SearchForm


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
        queryset = super().get_queryset().exclude(is_deleted=True).order_by('-created_at')
        if self.search_value:
            queryset = Resume.objects.filter(Q(title_job__icontains=self.search_value).order_by('-created_at'))
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
        print(request.POST)
        if form.is_valid():
            vacancy = Vacancy.objects.last()
            vacancy.title = request.POST['title']
            vacancy.salary_level = request.POST['salary_level']
            vacancy.text = request.POST['text']
            vacancy.experience_id = request.POST['experience']
            vacancy.specialization_id = request.POST['specialization']
            vacancy.save()
            return redirect('profile', pk=self.kwargs['pk'])
        context = {}
        context['form'] = form
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        Vacancy.objects.create(author=request.user)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VacancyCreateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})
