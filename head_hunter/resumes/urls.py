from django.urls import path
from resumes.views import ResumeCreateView, ResumeCreateExperienceView, ResumeCreateEducationView, \
    ResumeCreateCourseView, ResumePublicView, ResumeUpdateDateView


urlpatterns = [
    path('<int:pk>/create', ResumeCreateView.as_view(), name='resume_create'),
    path('<int:pk>/create/experience/', ResumeCreateExperienceView.as_view(), name='resume_experience_create'),
    path('<int:pk>/create/education/', ResumeCreateEducationView.as_view(), name='resume_education_create'),
    path('<int:pk>/create/course/', ResumeCreateCourseView.as_view(), name='resume_course_create'),
    path('<int:pk>/update_date/', ResumeUpdateDateView.as_view(), name='resume_date_update'),
    path('<int:pk>/update_date/', ResumePublicView.as_view(), name='resume_public'),

]