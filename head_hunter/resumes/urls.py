from django.urls import path
from resumes.views import ResumeCreateView, ResumeCreateExperienceView, ResumeCreateEducationView, \
    ResumeCreateCourseView, ResumePublicView, ResumeUpdateDateView, ResumeEditView, ResumeDetailView, \
    ResumeAddResponseView, ResumesResponsesView, ResumeAddChatMessageView

from vacancies.views.base import ResumesIndexView


urlpatterns = [
    path('resumes/<int:pk>', ResumesIndexView.as_view(), name='index_resumes'),
    path('resume/<int:pk>/detail/', ResumeDetailView.as_view(), name='resume_detail'),
    path('resume/<int:pk>/create', ResumeCreateView.as_view(), name='resume_create'),
    path('resume/<int:pk>/create/experience/', ResumeCreateExperienceView.as_view(), name='resume_experience_create'),
    path('resume/<int:pk>/create/education/', ResumeCreateEducationView.as_view(), name='resume_education_create'),
    path('resume/<int:pk>/create/course/', ResumeCreateCourseView.as_view(), name='resume_course_create'),
    path('resume/<int:pk>/update_date/', ResumeUpdateDateView.as_view(), name='resume_date_update'),
    path('resume/<int:pk>/public/', ResumePublicView.as_view(), name='resume_public'),
    path('resume/<int:pk>/edit', ResumeEditView.as_view(), name='resume_edit'),
    path('resume/<int:pk>/detail/add/response/', ResumeAddResponseView.as_view(), name='resume_add_response'),
    path('resume/<int:pk>/response/', ResumesResponsesView.as_view(), name='responses'),
    # path('resume/<int:pk>/to_vacancy_response/', ToVacancyResponsesView.as_view(), name='to_vacancy_responses'),
    path('resume/<int:pk>/response/add/chat_message/', ResumeAddChatMessageView.as_view(), name='add_chat_message'),
]
