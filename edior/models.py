from django.db import models


class Forms(models.Model):
    form_uid = models.CharField(verbose_name='form_uid', null=False, max_length=32)
    title = models.TextField(verbose_name='Название', null=False)
    data = models.DateTimeField(auto_now_add=True, verbose_name='время создания', null=False)

    class Meta:
        verbose_name = 'Форма'
        verbose_name_plural = 'Формы'


class Spaces(models.Model):
    form_uid = models.CharField(verbose_name='form_uid', max_length=32)
    unique_token = models.CharField(verbose_name='Уникальный токен', max_length=64)
    type = models.TextField(verbose_name='Тип поля')
    question = models.TextField(verbose_name='Вопрос', null=False)
    variants = models.TextField(verbose_name='Варианты ответа', null=True)

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'




