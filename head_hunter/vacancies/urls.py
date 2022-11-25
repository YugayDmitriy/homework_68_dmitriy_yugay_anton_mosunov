from django.urls import path
from vacancies.views.base import VacanciesIndexView, VacancyCreateView, ResumesIndexView,\
    VacancyPublicView, VacancyEditView, VacancyUpdateDateView, VacancyDetailView, VacancyAddResponseView, \
    ToVacanciesResponsesView, VacancyAddChatMessageView, vacancy_category_view, vacancy_salary_sort_view

urlpatterns = [
    path('', VacanciesIndexView.as_view(), name='index'),
    path('vacancy/<int:pk>/create', VacancyCreateView.as_view(), name='create_vacancy'),
    path('vacancy/<int:pk>/public/', VacancyPublicView.as_view(), name='vacancy_public'),
    path('vacancy/<int:pk>/edit', VacancyEditView.as_view(), name='vacancy_edit'),
    path('vacancy/<int:pk>/update_date/', VacancyUpdateDateView.as_view(), name='vacancy_date_update'),
    path('vacancy/<int:pk>/detail/', VacancyDetailView.as_view(), name='vacancy_detail'),
    path('vacancy/<int:pk>/detail/add/response/', VacancyAddResponseView.as_view(), name='vacancy_add_response'),
    path('vacancy/<int:pk>/response/', ToVacanciesResponsesView.as_view(), name='to_vacancies_responses'),
    path('vacancy/<int:pk>/response/add/vacancy_chat_message/', VacancyAddChatMessageView.as_view(), name='add_vacancy_chat_message'),
    path('vacancies/<str:category>', vacancy_category_view, name='list_by_vacancy_category'),
    path('vacancies/<int:choice>/salary', vacancy_salary_sort_view, name='vacancy_salary_sort'),
]
