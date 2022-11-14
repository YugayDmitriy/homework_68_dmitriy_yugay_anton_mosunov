from django.core.exceptions import ValidationError
from django.db import models

from django.core.validators import BaseValidator, MinValueValidator, MinLengthValidator
from django.utils.deconstruct import deconstructible


class Experience(models.Model):
    work_begin = models.DateField(
        verbose_name='Начало работы',
        max_length=200,
        null=True,
        blank=False
    )
    work_end = models.DateField(
        verbose_name='Окончание работы',
        max_length=200,
        null=True,
        blank=False
    )
    company = models.CharField(
        verbose_name='Название организации',
        max_length=200,
        null=True,
        blank=False,
        validators=[MinLengthValidator(0)],
    )
    job_title = models.CharField(
        verbose_name='Должность',
        max_length=200,
        null=True,
        blank=False,
    )
    responsibilities = models.TextField(
        verbose_name='Рабочие обязанности',
        max_length=3000,
        null=True,
        blank=False,
    )
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False, null=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    def __str__(self):
        return f'{self.company} {self.profession} {self.job_title} {self.salary_level} {self.work_begin} ' \
               f'{self.work_end} {self.responsibilities}'
