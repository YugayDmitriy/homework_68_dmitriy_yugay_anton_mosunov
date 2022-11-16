from django.contrib import admin
from vacancies.models.experiences import Experience
from vacancies.models.vacancies import Vacancy
from vacancies.models.specializations import Specialization


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary_level', 'text', 'experience', 'specialization')
    list_filter = ('title', 'salary_level', 'text', 'experience', 'specialization')
    search_fields = ('title', 'salary_level', 'text', 'experience', 'specialization')
    fields = ('title', 'salary_level', 'text', 'experience', 'specialization')
    readonly_fields = ['id']


admin.site.register(Vacancy, VacancyAdmin)


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('experience_name', 'created_at', 'updated_at', )
    list_filter = ('experience_name', 'created_at', 'updated_at', )
    search_fields = ('experience_name', 'created_at', 'updated_at', )
    fields = ('experience_name', 'created_at', 'updated_at', )
    readonly_fields = ['id']


admin.site.register(Experience)
admin.site.register(Specialization)


