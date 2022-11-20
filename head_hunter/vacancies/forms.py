from django import forms
from vacancies.models.experiences import Experience
from vacancies.models.vacancies import Vacancy
from vacancies.models.specializations import Specialization


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
