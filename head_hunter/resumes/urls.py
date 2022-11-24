from django.urls import path
from resumes.views import ResumeCreateView, ResumeCreateExperienceView, ResumeCreateEducationView, \
    ResumeCreateCourseView, ResumePublicView, ResumeUpdateDateView, ResumeEditView, ResumeDetailView, \
    ResumeAddResponseView, ResumesResponsesView, ResumeAddChatMessageView, ResumeDeleteView, ResumeEditExperienceView, \
    ResumeEditEducationView, ResumeEditCourseView, ResumeDeleteExperienceView, ResumeDeleteEducationView, \
    ResumeDeleteEducationView, ResumeDeleteCourseView, resume_category_view, resume_salary_sort_view

from vacancies.views.base import ResumesIndexView


urlpatterns = [
    path('resumes/<int:pk>', ResumesIndexView.as_view(), name='index_resumes'),
    path('resume/<int:pk>/detail/', ResumeDetailView.as_view(), name='resume_detail'),
    path('resume/<int:pk>/create', ResumeCreateView.as_view(), name='resume_create'),
    path('resume/<int:pk>/create/experience/', ResumeCreateExperienceView.as_view(), name='resume_experience_create'),
    path('resume/<int:pk>/edit/experience/', ResumeEditExperienceView.as_view(), name='resume_experience_edit'),
    path('resume/<int:pk>/delete/experience/', ResumeDeleteExperienceView.as_view(), name='resume_experience_delete'),
    path('resume/<int:pk>/experience/confirm-delete/', ResumeDeleteExperienceView.as_view(), name='experience_confirm_delete'),
    path('resume/<int:pk>/edit/education/', ResumeEditEducationView.as_view(), name='resume_education_edit'),
    path('resume/<int:pk>/delete/education/', ResumeDeleteEducationView.as_view(), name='resume_education_delete'),
    path('resume/<int:pk>/education/confirm-delete/', ResumeDeleteEducationView.as_view(), name='education_confirm_delete'),
    path('resume/<int:pk>/edit/course/', ResumeEditCourseView.as_view(), name='resume_course_edit'),
    path('resume/<int:pk>/delete/course/', ResumeDeleteCourseView.as_view(), name='resume_course_delete'),
    path('resume/<int:pk>/course/confirm-delete/', ResumeDeleteCourseView.as_view(), name='course_confirm_delete'),
    path('resume/<int:pk>/create/education/', ResumeCreateEducationView.as_view(), name='resume_education_create'),
    path('resume/<int:pk>/create/course/', ResumeCreateCourseView.as_view(), name='resume_course_create'),
    path('resume/<int:pk>/update_date/', ResumeUpdateDateView.as_view(), name='resume_date_update'),
    path('resume/<int:pk>/public/', ResumePublicView.as_view(), name='resume_public'),
    path('resume/<int:pk>/edit', ResumeEditView.as_view(), name='resume_edit'),
    path('resume/<int:pk>/detail/add/response/', ResumeAddResponseView.as_view(), name='resume_add_response'),
    path('resume/<int:pk>/response/', ResumesResponsesView.as_view(), name='responses'),
    path('resume/<int:pk>/confirm-delete/', ResumeDeleteView.as_view(), name='resume_confirm_delete'),
    path('resume/<int:pk>/delete/', ResumeDeleteView.as_view(), name='resume_delete'),
    path('resume/<int:pk>/response/add/chat_message/', ResumeAddChatMessageView.as_view(), name='add_chat_message'),
    path('resumes/<str:category>', resume_category_view, name='list_by_resume_category'),
    path('resumes/<int:choice>/salary', resume_salary_sort_view, name='salary_sort'),
]
