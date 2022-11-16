from django.urls import path
from vacancies.views.base import VacanciesIndexView, VacancyCreateView


urlpatterns = [
    path('', VacanciesIndexView.as_view(), name='index'),
    path('<int:pk>/create', VacancyCreateView.as_view(), name='create_vacancy')
]
