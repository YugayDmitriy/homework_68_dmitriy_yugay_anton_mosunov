from django.contrib.auth import get_user_model
from django.db import models


class VacancyResponse(models.Model):
    author = models.ForeignKey(verbose_name='Автор отклика', to=get_user_model(), related_name='vacancy_responses', null=False,
                               blank=False,
                               on_delete=models.CASCADE)
    resume = models.ForeignKey(verbose_name='Резюме', to='resumes.Resume', related_name='vacancy_responses', null=False,
                             blank=False, on_delete=models.CASCADE)
    hello_message = models.TextField(verbose_name='Приветственное сообщение', null=False, blank=True, max_length=3000,
                                     default='Здравствуйте. Меня заинтересовала ваша вакансия!')
    vacancy = models.ForeignKey(
        to='vacancies.Vacancy',
        verbose_name='Вакансия',
        related_name='vacancy_responses',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалено',
        default=False, null=False
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    changed_at = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True
    )
