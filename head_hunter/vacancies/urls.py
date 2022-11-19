from django.urls import path
from vacancies.views.base import VacanciesIndexView, VacancyCreateView, ResumesIndexView,\
    VacancyPublicView, VacancyEditView, VacancyUpdateDateView, VacancyDetailView

urlpatterns = [
    path('', VacanciesIndexView.as_view(), name='index'),
    path('vacancy/<int:pk>/create', VacancyCreateView.as_view(), name='create_vacancy'),
    path('vacancy/<int:pk>/public/', VacancyPublicView.as_view(), name='vacancy_public'),
    path('vacancy/<int:pk>/edit', VacancyEditView.as_view(), name='vacancy_edit'),
    path('vacancy/<int:pk>/update_date/', VacancyUpdateDateView.as_view(), name='vacancy_date_update'),
    path('vacancy/<int:pk>/detail/', VacancyDetailView.as_view(), name='vacancy_detail'),
]
