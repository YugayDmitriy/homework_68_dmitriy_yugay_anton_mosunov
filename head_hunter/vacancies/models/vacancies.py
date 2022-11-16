from django.contrib.auth import get_user_model
from django.db import models
import uuid


class Vacancy(models.Model):
    author = models.ForeignKey(
        verbose_name='Автор вакансии',
        to=get_user_model(),
        related_name='vacancies',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    title = models.CharField(verbose_name='Наименование вакансии', max_length=100)
    salary_level = models.FloatField(verbose_name='Уровень зарплаты', null=True, blank=False)
    text = models.TextField(verbose_name='Описание вакансии', null=True, blank=True)
    experience = models.ForeignKey(
        to='vacancies.Experience',
        verbose_name='Опыт',
        related_name='vacancy',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    specialization = models.ForeignKey(
        to='vacancies.Specialization',
        verbose_name='Cпециализация',
        related_name='vacancy',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    is_public = models.BooleanField(verbose_name='Не опубликовано', default=False, null=False)
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False, null=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.salary_level} - {self.text} - {self.experience} - {self.specialization}"

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
