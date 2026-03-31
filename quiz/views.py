from django.shortcuts import render
from django.http import HttpResponse

from .models import Quiz, QuizPass, Question, QuestionAnswer, QuestionOption


def index_view(request)->HttpResponse:
    """Главная страница"""

    quiz_list = Quiz.objects.filter(status='open').values_list('name', flat=True)
    
    return render(template_name='quiz/index.html', request=request, context={'quiz_list': quiz_list})


def get_next_question(request, quiz_id=None)->HttpResponse:
    """ View для получения следующего вопроса """
    # проверка на дурака
    if not quiz_id:
        # return HttpResponse('quiz ID is require!', content_type='text/plain; charset=utf-8')
        return render(request=request, template_name='quiz/error.html', context={"error_text": f"quiz ID is require!"})

    # проверка что пользователь аутентифицирован
    if not request.user.is_authenticated:
        # return HttpResponse('You are not login! Please login', content_type='text/plain; charset=utf-8')
        return render(request=request, template_name='quiz/error.html', context={"error_text": f"You are not login! Please login"})


    # текущий пользователь
    current_user = request.user
    
    # проверка что пользователь проходит опрос
    try:
        quiz_pass = QuizPass.objects.get(quiz_id=quiz_id, resp_user=current_user, status='in_progress')

    except QuizPass.DoesNotExist:
        # return HttpResponse('You are not started this quiz!', content_type='text/plain; charset=utf-8')
        return render(request=request, template_name='quiz/error.html', context={"error_text": f"You are not started this quiz!"})

    
    # вытащим вопросы опроса
    question_of_quiz = Question.objects.filter(quiz_id=quiz_id).values_list('id', flat=True)
    
    # вытащим вопросы на которые уже дан ответ
    user_answers = QuestionAnswer.objects.filter(resp_user=current_user, question_id__in=question_of_quiz).values_list('question_id', flat=True)
    
    # вытащим следующий вопрос
    next_question = Question.objects.filter(quiz_id=quiz_id).exclude(id__in=user_answers).first()

    # есил вопроса нет, то пустое сообщение
    if not next_question:
        # return HttpResponse('You have already passed this quiz!', content_type='text/plain; charset=utf-8')
        return render(request=request, template_name='quiz/error.html', context={"error_text": f"You have already passed this quiz!"})


    # вытащим варианты ответов на следующий вопрос
    question_options = QuestionOption.objects.filter(question_id=next_question)

    # подготовим ответ
    ret = f"Следующий вопрос № {next_question.id}  \n\r {next_question.name} \n\r"
    if not question_options:
        ret += "Вариантов нет. Ожидаем ввод текста"
    else:
        ret += "Варианты: \n\r"
        for opt in question_options:
            ret += f"{opt.name} \n\r"

    return HttpResponse(ret, content_type='text/plain; charset=utf-8')
    
    



