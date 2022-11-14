from django.core.exceptions import ValidationError
from django.db import models

from django.core.validators import BaseValidator, MinValueValidator
from django.utils.deconstruct import deconstructible


class Education(models.Model):
    education_begin = models.DateField(
        verbose_name='Начало обучения',
        max_length=200,
        null=True,
        blank=False
    )
    education_end = models.DateField(
        verbose_name='Окончание обучения',
        max_length=200,
        null=True,
        blank=False
    )
    educational_institution_name = models.CharField(
        verbose_name='Название организации',
        max_length=200,
        null=True,
        blank=False
    )
    faculty = models.CharField(
        verbose_name='Факультет',
        max_length=200,
        null=True,
        blank=False
    )
    speciality = models.CharField(
        verbose_name='Полученная специальность',
        max_length=200,
        null=True,
        blank=False
    )
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False, null=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    def __str__(self):
        return f'{self.educational_institution} {self.faculty} {self.speciality} {self.education_begin} ' \
               f'{self.education_end} '
