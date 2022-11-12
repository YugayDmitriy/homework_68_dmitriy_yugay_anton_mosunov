# from django.shortcuts import render, redirect
from django.views.generic import ListView

from accounts.models import Account


# from django.db.models import Q
# from posts.models import Post
#
# from accounts.forms import SearchForm
#
# from accounts.models import Account
#
# from accounts.forms import CommentForm
#
# from posts.models import Comment

class VacanciesIndexView(ListView):
    template_name = 'index.html'
    model = Account
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacanciesIndexView, self).get_context_data(object_list=object_list, **kwargs)
        vacancies = Account.objects.all().order_by('-created_at')
        context['vacancies'] = vacancies
        return context

# class VacanciesIndexView(ListView):
#     template_name = 'index.html'
#     model = Vacancy
#     context_object_name = 'vacancies'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(VacanciesIndexView, self).get_context_data(object_list=object_list, **kwargs)
#         vacancies = Vacancy.objects.all().order_by('-created_at')
#         context['vacancies'] = vacancies
#         return context
