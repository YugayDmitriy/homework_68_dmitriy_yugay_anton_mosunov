from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import BaseValidator, MinValueValidator, MinLengthValidator
from django.utils.deconstruct import deconstructible


class Resume(models.Model):
    profession = models.ForeignKey(
        to='resumes.Profession',
        verbose_name='Профессия',
        related_name='resumes',
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        validators=[MinLengthValidator(0)],
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
    place_of_work = models.ForeignKey(
        to='resumes.Experience',
        verbose_name='Место работы',
        related_name='resumes',
        null=True,
        on_delete=models.CASCADE
    )
    educational_institution = models.ForeignKey(
        to='resumes.Education',
        verbose_name='Учебное заведение',
        related_name='resumes',
        null=True,
        on_delete=models.CASCADE
    )
    courses = models.ForeignKey(
        to='resumes.Course',
        verbose_name='Курсы',
        related_name='resumes',
        null=True,
        on_delete=models.CASCADE
    )
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False, null=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)


    def __str__(self):
        return f'{self.profession} {self.job_title} {self.salary_level} {self.about_user} {self.email} ' \
               f'{self.telegram_link} {self.Linkedin_link} {self.facebook_link} ' \
               f'{self.place_of_work} {self.educational_institution}'

