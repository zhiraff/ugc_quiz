import uuid

from django.db import models
from django.contrib.auth import get_user_model

from .enums import quiz_status, question_types, quiz_pass_status


User = get_user_model()

__all__ = ['Quiz', 'Question', 'QuestionOption', 'QuizPass', 'QuestionAnswer']


class Quiz(models.Model):
    """Опросы"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(verbose_name='Название')
    status = models.CharField(max_length=32, verbose_name='Статус опроса', default='draft', choices=quiz_status)
    owner_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name="Автор опроса", default=None)
    pass_count = models.IntegerField(verbose_name='Количество пользователей прошедших опрос', default=0)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    
    def __str__(self):
        return f"{self.name[:50]} : {self.status}"

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        unique_together = ['name', 'owner_user']


class Question(models.Model):
    """Вопросы"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="ID опроса")
    name = models.TextField(verbose_name='Текст вопроса')
    q_type = models.CharField(max_length=32, verbose_name='Тип вопроса', default='free_text', choices=question_types)
    rank = models.SmallIntegerField(verbose_name='Ранк вопроса', default=999, help_text='Чем меньше это число, тем выше вопрос в списке')
    
    def __str__(self):
        return f"{self.name[:50]} : {self.rank}"

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['rank']


class QuestionOption(models.Model):
    """Варианты ответов на вопросы"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="ID вопроса")
    name = models.TextField(verbose_name='Текст ответа')
    choice_count = models.IntegerField(verbose_name='Сколько раз выбрали', default=0)
    rank = models.SmallIntegerField(verbose_name='Ранк варианта', default=999, help_text='Чем меньше это число, тем выше вариант в списке')
    
    def __str__(self):
        return f"{self.name[:50]} : {self.rank}"

    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'
        ordering = ['rank']


class QuizPass(models.Model):
    """Прохождение опросов"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="ID опроса")
    status = models.CharField(max_length=32, verbose_name='Статус прохождения', default='not_started', choices=quiz_pass_status)
    resp_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name="Пользователь", default=None)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    
    def __str__(self):
        return f"{self.quiz_id.name} : {self.resp_user.username}"

    class Meta:
        verbose_name = 'Прохождение'
        verbose_name_plural = 'Прохождения'
        unique_together = ['quiz_id', 'resp_user']


class QuestionAnswer(models.Model):
    """Ответы пользователей на вопросы"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="ID вопроса")
    resp_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name="Пользователь", default=None)
    answer = models.TextField(verbose_name='Текст ответа', blank=True, null=True)
    asnwer_option_id = models.ForeignKey(QuestionOption, on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name="Выбранный ответ", default=None)
    
    def __str__(self):
        return f"{self.question_id.name} : {self.resp_user.username} : {self.answer[:50]} : {self.asnwer_option_id.name if self.asnwer_option_id else ''}"

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'