from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView
from accounts.models import Account
from vacancies.models.vacancies import Vacancy
from vacancies.forms import VacancyForm

from resumes.models import Resume


# from django.db.models import Q
# from posts.models import Post
#
# from accounts.forms import SearchForm
#
# from accounts.models import Account
#
# from accounts.forms import CommentForm
#
# from posts.models import Comment

class VacanciesIndexView(ListView):
    template_name = 'index.html'
    model = Vacancy
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacanciesIndexView, self).get_context_data(object_list=object_list, **kwargs)
        vacancies = Vacancy.objects.all().order_by('-created_at')
        context['vacancies'] = vacancies
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
