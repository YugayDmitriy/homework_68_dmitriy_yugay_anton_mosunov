from django.core.exceptions import ValidationError
from django.db import models

from django.core.validators import BaseValidator, MinValueValidator
from django.utils.deconstruct import deconstructible


class Course(models.Model):
    resume = models.ForeignKey(
        verbose_name='Резюме',
        to='resumes.Resume',
        related_name='cources',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    course_name = models.CharField(
        verbose_name='Полученная специальность',
        max_length=200,
        null=True,
        blank=False
    )
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False, null=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    def __str__(self):
        return f'{self.course_name} '
