from django.utils import timezone

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import BaseValidator, MinValueValidator, MinLengthValidator
from django.utils.deconstruct import deconstructible


class Resume(models.Model):
    author = models.ForeignKey(
        verbose_name='Автор резюме',
        to=get_user_model(),
        related_name='resumes',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    profession = models.ForeignKey(
        to='resumes.Profession',
        verbose_name='Профессия',
        related_name='resumes',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    job_title = models.CharField(
        verbose_name='Должность',
        max_length=200,
        null=True,
        blank=False
    )
    salary_level = models.FloatField(
        verbose_name='Уровень зарплаты',
        null=True,
        blank=False
    )
    about_user = models.TextField(
        verbose_name='Информация о себе',
        max_length=3000,
        null=True,
        blank=False
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        null=True,
        blank=False,
    )
    phone = PhoneNumberField(
        unique=False,
        null=True,
        blank=False
    )
    telegram_link = models.CharField(
        verbose_name='Telegram',
        max_length=200,
        null=True,
        blank=False
    )
    linkedin_link = models.CharField(
        verbose_name='Linkedin',
        max_length=200,
        null=True,
        blank=False
    )
    facebook_link = models.CharField(
        verbose_name='Facebook',
        max_length=200,
        null=True,
        blank=False
    )
    is_public = models.BooleanField(verbose_name='Не опубликовано', default=False, null=False)
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False, null=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)


    def __str__(self):
        return f'{self.profession} {self.job_title} {self.salary_level} {self.about_user} {self.email} ' \
               f'{self.telegram_link} {self.linkedin_link} {self.facebook_link} '




