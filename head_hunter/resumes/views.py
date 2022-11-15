from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from resumes.forms import ResumeForm

from resumes.models import Resume

from resumes.forms import ExperienceForm

from resumes.forms import EducationForm

from resumes.forms import CourseForm

from resumes.models import Experience

from resumes.models import Education

from resumes.models import Course


class ResumeCreateView(CreateView):
    template_name = 'resume_create.html'
    form_class = ResumeForm
    model = Resume

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            resume = Resume.objects.update(profession=request.POST['profession'],
                                           job_title=request.POST['job_title'],
                                           salary_level=request.POST['salary_level'],
                                           about_user=request.POST['about_user'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            telegram_link=request.POST['telegram_link'],
            linkedin_link=request.POST['linkedin_link'],
            facebook_link=request.POST['facebook_link'])
            # form.instance.author_id = self.kwargs['pk']
            # form.save()
            return redirect('profile', pk=self.kwargs['pk'])
        context = {}
        context['form'] = form
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        Resume.objects.create(author=request.user)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ResumeCreateView, self).get_context_data(**kwargs)
        context['experience_form'] = ExperienceForm()
        context['education_form'] = EducationForm()
        context['course_form'] = CourseForm()
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
        resume = Resume.objects.last()
        work_begin = request.POST['work_begin']
        Experience.objects.create(resume=resume, work_begin=work_begin, work_end=work_end,
                                  company=company, job_title=job_title, responsibilities=responsibilities)
        context = {}
        return self.render_to_response(context)


class ResumeCreateEducationView(CreateView):
    model = Education

    def post(self, request, *args, **kwargs):
        print(request.POST)
        education_begin = request.POST['education_begin']
        education_end = request.POST['education_end']
        educational_institution_name = request.POST['educational_institution_name']
        faculty = request.POST['faculty']
        speciality = request.POST['speciality']
        resume = Resume.objects.last()
        Education.objects.create(resume=resume, education_begin=education_begin, education_end=education_end,
                                 educational_institution_name=educational_institution_name, faculty=faculty,
                                 speciality=speciality)
        context = {}
        return self.render_to_response(context)


class ResumeCreateCourseView(CreateView):
    model = Course

    def post(self, request, *args, **kwargs):
        course_name = request.POST['course_name']
        resume = Resume.objects.last()
        Course.objects.create(resume=resume, course_name=course_name)
        context = {}
        return self.render_to_response(context)
