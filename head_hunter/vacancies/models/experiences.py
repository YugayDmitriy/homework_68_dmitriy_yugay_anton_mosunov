from django.db import models


class Experience(models.Model):
    experience_name = models.CharField(
        verbose_name='Опыт',
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
        return self.experience_name

    class Meta:
        verbose_name = 'Опыт'
        verbose_name_plural = 'Опыт'
