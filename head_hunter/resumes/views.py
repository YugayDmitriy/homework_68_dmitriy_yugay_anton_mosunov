from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView
from datetime import datetime

from resumes.models import Resume, Experience, Education, Course
from resumes.forms import ExperienceForm, EducationForm, CourseForm, ResumeForm


class ResumeCreateView(CreateView):
    template_name = 'resume_create.html'
    form_class = ResumeForm
    model = Resume



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
        print(f' pk резюме {kwargs["pk"]}')
        print(f' Пришедший запрос {request.POST}')
        print(f'Резюме из списка {resume.pk}')

        Experience.objects.create(resume=resume, work_begin=work_begin, work_end=work_end,
                                  company=company, job_title=job_title, responsibilities=responsibilities)

        return HttpResponse('success')


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


class ResumeCreateCourseView(CreateView):
    model = Course

    def post(self, request, *args, **kwargs):
        course_name = request.POST['course_name']
        resume = Resume.objects.get(pk=kwargs['pk'])
        Course.objects.create(resume=resume, course_name=course_name)
        return HttpResponse('success')


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


class ResumeEditView(UpdateView):
    template_name = 'resume_edit.html'
    form_class = ResumeForm
    model = Resume
    context_object_name = 'resume'

    def get_context_data(self, **kwargs):
        context = super(ResumeEditView, self).get_context_data(**kwargs)
        context['form'] = ResumeForm(instance=self.object)
        resume = self.object
        context['experience_form'] = ExperienceForm()
        context['education_form'] = EducationForm()
        context['course_form'] = CourseForm()
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


class ResumeDetailView(DetailView):
    template_name = 'resume_detail.html'
    model = Resume
    context_object_name = 'resume'

    def get_context_data(self,  **kwargs):
        context = super(ResumeDetailView, self).get_context_data(**kwargs)
        experiences = Experience.objects.filter(resume_id=self.object.pk)
        education = Education.objects.filter(resume_id=self.object.pk)
        courses = Course.objects.filter(resume_id=self.object.pk)
        # context['comment_form'] = CommentForm()
        context['experiences'] = experiences
        context['education'] = education
        context['courses'] = courses
        return context
