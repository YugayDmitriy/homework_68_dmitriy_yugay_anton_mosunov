from django import forms
from vacancies.models.experiences import Experience
from vacancies.models.vacancies import Vacancy
from vacancies.models.specializations import Specialization

from resumes.models import Resume

from vacancies.models import VacancyResponse


class VacancyForm(forms.ModelForm):
    title = forms.CharField(
        label='Название вакансии',
        max_length=100,
        )

    text = forms.CharField(
        label='Описание',
        widget=forms.Textarea
    )

    experience = forms.ModelChoiceField(
        queryset=Experience.objects.all(),
        empty_label='Опыт не выбран'),

    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        empty_label='Специализация не выбрана'
    )

    class Meta:
        model = Vacancy
        fields = ('title', 'salary_level', 'text', 'experience', 'specialization')


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='')


class VacancyResponseForm(forms.ModelForm):

    def __init__(self, current_user, *args, **kwargs):
        super(VacancyResponseForm, self).__init__(*args, **kwargs)
        self.fields['resume'].queryset = self.fields['resume'].queryset.filter(author=current_user.pk)

    hello_message = forms.CharField(max_length=3000, required=True, label='Приветственное сообщение',
                              widget=forms.Textarea(attrs={'name': 'body', 'rows': 5, 'cols': 21}))
    resume = forms.ModelChoiceField(
        label='Необходимо выбрать резюме',
        queryset=Resume.objects.all(),
    )

    class Meta:
        model = VacancyResponse
        widgets = {
            'message': forms.Textarea(attrs={'cols': 21, 'rows': 5}),
        }
        fields = ('hello_message', 'resume', )


class ChatForm(forms.Form):
    message = forms.CharField(max_length=3000, required=False, label='',
                              widget=forms.Textarea(attrs={'name': 'body', 'rows': 3, 'cols': 21}))


class VacancyChatForm(forms.Form):
    message = forms.CharField(max_length=3000, required=False, label='',
                              widget=forms.Textarea(attrs={'name': 'body', 'rows': 3, 'cols': 21}))

