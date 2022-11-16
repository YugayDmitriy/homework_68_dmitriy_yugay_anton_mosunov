from django.db import models


class Specialization(models.Model):
    specialization_name = models.CharField(
        verbose_name='Специализация',
        max_length=100,
        null=True,
        blank=False
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True
    )

    def __str__(self):
        return self.specialization_name

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
