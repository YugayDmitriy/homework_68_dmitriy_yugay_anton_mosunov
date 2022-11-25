from django.contrib import admin
from resumes.models import Resume, Experience, Profession, Education

admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(Profession)
admin.site.register(Education)
