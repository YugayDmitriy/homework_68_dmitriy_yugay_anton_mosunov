from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, ListView, DeleteView
from datetime import datetime

from resumes.models import Resume, Experience, Education, Course, Response, Chat
from resumes.forms import ExperienceForm, EducationForm, CourseForm, ResumeForm, ResponseForm, ChatForm

from vacancies.models import Vacancy

from vacancies.forms import VacancyChatForm

from vacancies.forms import SearchForm

from resumes.models import Profession


class ResumeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'resume_create.html'
    form_class = ResumeForm
    model = Resume
    permission_required = 'resumes.add_resume'


    def get(self, request, *args, **kwargs):
        resume = Resume.objects.create(author=request.user)
        # return super().get(request, *args, **kwargs)
        return redirect('resume_edit', pk=resume.pk)

    def get_context_data(self, **kwargs):
        context = super(ResumeCreateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


class ResumeCreateExperienceView(CreateView):
    model = Experience

    def post(self, request, *args, **kwargs):
        work_begin = request.POST['work_begin']
        work_end = request.POST['work_end']
        company = request.POST['company']
        job_title = request.POST['job_title']
        responsibilities = request.POST['responsibilities']

        resume = Resume.objects.get(pk=kwargs['pk'])
        Experience.objects.create(resume=resume, work_begin=work_begin, work_end=work_end,
                                  company=company, job_title=job_title, responsibilities=responsibilities)
        return HttpResponse('success')


class ResumeEditExperienceView(UpdateView):
    template_name = 'experience_edit.html'
    form_class = ExperienceForm
    model = Experience
    context_object_name = 'experience'

    def get_context_data(self, **kwargs):
        context = super(ResumeEditExperienceView, self).get_context_data(**kwargs)
        context['experience_form'] = ExperienceForm(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('resume_edit', pk=self.object.resume.pk)


class ResumeDeleteExperienceView(DeleteView):
    template_name = 'experience_confirm_delete.html'
    model = Experience

    def form_valid(self, form):
        pk = self.object.resume.pk
        self.object.delete()
        return redirect('resume_edit', pk=pk)


class ResumeCreateEducationView(CreateView):
    model = Education

    def post(self, request, *args, **kwargs):
        education_begin = request.POST['education_begin']
        education_end = request.POST['education_end']
        educational_institution_name = request.POST['educational_institution_name']
        faculty = request.POST['faculty']
        speciality = request.POST['speciality']
        resume = Resume.objects.get(pk=kwargs['pk'])
        Education.objects.create(resume=resume, education_begin=education_begin, education_end=education_end,
                                 educational_institution_name=educational_institution_name, faculty=faculty,
                                 speciality=speciality)
        return HttpResponse('success')


class ResumeEditEducationView(UpdateView):
    template_name = 'education_edit.html'
    form_class = EducationForm
    model = Education
    context_object_name = 'education'

    def get_context_data(self, **kwargs):
        context = super(ResumeEditEducationView, self).get_context_data(**kwargs)
        context['education_form'] = EducationForm(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('resume_edit', pk=self.object.resume.pk)


class ResumeDeleteEducationView(DeleteView):
    template_name = 'education_confirm_delete.html'
    model = Education

    def form_valid(self, form):
        pk = self.object.resume.pk
        self.object.delete()
        return redirect('resume_edit', pk=pk)


class ResumeCreateCourseView(CreateView):
    model = Course

    def post(self, request, *args, **kwargs):
        course_name = request.POST['course_name']
        resume = Resume.objects.get(pk=kwargs['pk'])
        Course.objects.create(resume=resume, course_name=course_name)
        return HttpResponse('success')


class ResumeEditCourseView(UpdateView):
    template_name = 'course_edit.html'
    form_class = CourseForm
    model = Course
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super(ResumeEditCourseView, self).get_context_data(**kwargs)
        context['course_form'] = CourseForm(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('resume_edit', pk=self.object.resume.pk)


class ResumeDeleteCourseView(DeleteView):
    template_name = 'course_confirm_delete.html'
    model = Course

    def form_valid(self, form):
        pk = self.object.resume.pk
        self.object.delete()
        return redirect('resume_edit', pk=pk)


class ResumeUpdateDateView(TemplateView):
    model = Resume


    def post(self, request, *args, **kwargs):
        resume = Resume.objects.get(id=kwargs['pk'])
        resume.changed_at = datetime.now()
        resume.save()
        return redirect('profile', pk=request.user.pk)


class ResumePublicView(TemplateView):
    model = Resume

    def post(self, request, *args, **kwargs):
        resume = Resume.objects.get(id=kwargs['pk'])
        if resume.is_public:
            resume.is_public = False
            resume.save()
            return redirect('profile', pk=request.user.pk)
        if not resume.is_public:
            resume.is_public = True
            resume.save()
        return redirect('profile', pk=request.user.pk)


class ResumeEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'resume_edit.html'
    form_class = ResumeForm
    model = Resume
    context_object_name = 'resume'
    permission_required = 'resumes.change_vacancy'

    def has_permission(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        experiences = Experience.objects.filter(resume_id=self.object.pk)
        education = Education.objects.filter(resume_id=self.object.pk)
        courses = Course.objects.filter(resume_id=self.object.pk)
        context = super(ResumeEditView, self).get_context_data(**kwargs)
        context['experiences'] = experiences
        context['education'] = education
        context['courses'] = courses

        context['form'] = ResumeForm(instance=self.object)
        resume = self.object
        context['experience_form'] = ExperienceForm()
        context['education_form'] = EducationForm()
        context['course_form'] = CourseForm()
        # experience = Experience.objects.filter
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST, request.FILES)
        print(kwargs['pk'])
        if form.is_valid():
            resume = Resume.objects.get(pk=kwargs['pk'])
            resume.profession_id = request.POST['profession']
            resume.job_title = request.POST['job_title']
            resume.salary_level = request.POST['salary_level']
            resume.about_user = request.POST['about_user']
            resume.email = request.POST['email']
            resume.phone = request.POST['phone']
            resume.telegram_link = request.POST['telegram_link']
            resume.linkedin_link = request.POST['linkedin_link']
            resume.facebook_link = request.POST['facebook_link']
            resume.save()
            return redirect('profile', pk=self.request.user.pk)
        context = {}
        context['form'] = form
        return self.render_to_response(context)

    def get_success_url(self, request):
        return reverse('profile', kwargs={'pk': self.object.author})


class ResumeDetailView(LoginRequiredMixin, DetailView):
    template_name = 'resume_detail.html'
    model = Resume
    context_object_name = 'resume'

    def get_context_data(self,  **kwargs):
        context = super(ResumeDetailView, self).get_context_data(**kwargs)
        experiences = Experience.objects.filter(resume_id=self.object.pk)
        education = Education.objects.filter(resume_id=self.object.pk)
        courses = Course.objects.filter(resume_id=self.object.pk)
        vacancies = Vacancy.objects.exclude(is_deleted=True).exclude(is_public=False)
        context['vacancies'] = vacancies
        context['response_form'] = ResponseForm(current_user=self.request.user)
        context['experiences'] = experiences
        context['education'] = education
        context['courses'] = courses
        return context


class ResumeAddResponseView(LoginRequiredMixin, CreateView):
    model = Response

    def post(self, request, *args, **kwargs):
        print(request.POST)
        hello_message = request.POST['hello_message']
        resume = Resume.objects.get(pk=kwargs['pk'])
        author = request.user
        vacancy = request.POST['vacancy']
        Response.objects.create(resume=resume, author=author, hello_message=hello_message, vacancy_id=vacancy)
        return HttpResponse('success')


class ResumesResponsesView(LoginRequiredMixin, ListView):
    template_name = 'resumes_responses.html'
    model = Resume
    context_object_name = 'resumes'
    permission_required = 'resumes.view_response'



    def get(self, request, *args, **kwargs):
        self.form = ChatForm()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True).order_by('-created_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResumesResponsesView, self).get_context_data(object_list=object_list, **kwargs)
        context['chat_form'] = self.form
        return context


class ResumeAddChatMessageView(CreateView):
    model = Chat
    form_class = ChatForm

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(kwargs['pk'])
        message = request.POST['message']
        response = Response.objects.get(pk=kwargs['pk'])
        author = self.request.user
        Chat.objects.create(response=response, message=message, author=author)
        return redirect('responses', pk=self.request.user.pk)


class ResumeDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'resume_confirm_delete.html'
    model = Resume
    permission_required = 'resumes.delete_resume'

    def has_permission(self):
        return self.get_object().author == self.request.user

    def post(self, request, *args, **kwargs):
        resume = Resume.objects.get(pk=kwargs['pk'])
        resume.deleted_at = timezone.now()
        resume.is_deleted = True
        resume.save()
        return redirect('profile', pk=self.request.user.pk)


def resume_category_view(request, category):
    form = SearchForm(request.GET)
    search_value = get_search_value(form)
    professions = Profession.objects.all()
    if search_value:
        resumes = Resume.objects.filter(Q(job_title__icontains=search_value))
        context = {
            'form': SearchForm(),
            'resumes': resumes,
            'professions': professions
        }
        return render(request, 'index_resumes.html', context)
    profession = Profession.objects.get(profession_name=category)
    resumes = Resume.objects.filter(profession=profession.pk, is_deleted=False).order_by('changed_at')
    find_form = SearchForm()
    context = {
        'form': find_form,
        'resumes': resumes,
        'professions': professions
    }
    return render(request, 'index_resumes.html', context)


def get_search_value(form):
    if form.is_valid():
        return form.cleaned_data.get('search')
    return None


def resume_salary_sort_view(request, choice):
    form = SearchForm(request.GET)
    search_value = get_search_value(form)
    professions = Profession.objects.all()

    if search_value:
        if choice == 1:
            resumes = Resume.objects.filter(Q(job_title__icontains=search_value)).order_by('salary_level')
        elif choice == 0:
            resumes = Resume.objects.filter(Q(job_title__icontains=search_value)).order_by('-salary_level')
        context = {
            'form': SearchForm(),
            'resumes': resumes,
            'professions': professions
        }
        return render(request, 'index_resumes.html', context)
    if choice == 1:
        resumes = Resume.objects.filter(is_deleted=False).order_by('salary_level')
    elif choice == 0:
        resumes = Resume.objects.filter(is_deleted=False).order_by('-salary_level')
    find_form = SearchForm()
    context = {
        'form': find_form,
        'resumes': resumes,
        'professions': professions
    }
    return render(request, 'index_resumes.html', context)