from django.urls import path
from vacancies.views.base import VacanciesIndexView, VacancyCreateView, ResumesIndexView

urlpatterns = [
    path('', VacanciesIndexView.as_view(), name='index'),
    path('<int:pk>/create', VacancyCreateView.as_view(), name='create_vacancy'),
    path('resumes/<int:pk>', ResumesIndexView.as_view(), name='index_resumes')
]
