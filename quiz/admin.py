from django.contrib import admin

from .models import Quiz, Question, QuestionOption, QuizPass, QuestionAnswer

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(QuizPass)
admin.site.register(QuestionAnswer)
