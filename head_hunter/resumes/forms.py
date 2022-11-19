from django import forms

from resumes.models import Resume, Profession, Experience, Education, Course


class ResumeForm(forms.ModelForm):
    profession = forms.ModelChoiceField(
        label='Выберите профессию',
        queryset=Profession.objects.all(),
    )

    class Meta:
        model = Resume
        widgets = {
            'about_user': forms.Textarea(attrs={'cols': 21, 'rows': 5}),
        }
        fields = ('profession', 'job_title', 'salary_level', 'about_user', 'email',
                  'phone', 'telegram_link', 'linkedin_link', 'facebook_link')


class ExperienceForm(forms.ModelForm):
    company = forms.CharField(label='Название компании', required=False)
    job_title = forms.CharField(label='Позиция', required=False, )
    responsibilities = forms.CharField(
        label='Рабочие обязанности', required=False,
        widget=forms.Textarea(attrs={'name': 'body', 'rows': 5, 'cols': 21})
    )
    work_begin = forms.DateField(label='Начало работы', widget=forms.SelectDateWidget)
    work_end = forms.DateField(label='Окончание работы', widget=forms.SelectDateWidget)

    class Meta:
        model = Experience
        fields = ('company', 'work_begin', 'work_end', 'job_title', 'responsibilities', )


class EducationForm(forms.ModelForm):
    responsibilities = forms.CharField(
        label='Информация о себе',
        widget=forms.Textarea(attrs={'name': 'body', 'rows': 5, 'cols': 21})
    )
    education_begin = forms.DateField(label='Начало обучения', widget=forms.SelectDateWidget)
    education_end = forms.DateField(label='Окончание обучения', widget=forms.SelectDateWidget)

    class Meta:
        model = Education
        fields = ('educational_institution_name', 'faculty', 'speciality', 'education_begin', 'education_end', )


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('course_name', )


class ResponseForm(forms.Form):
    message = forms.CharField(max_length=3000, required=True, label='Сообщение',
                              widget=forms.Textarea(attrs={'name': 'body', 'rows': 5, 'cols': 21}))

    class Meta:
        widgets = {
            'message': forms.Textarea(attrs={'cols': 21, 'rows': 5}),
        }
        fields = ('message',)
