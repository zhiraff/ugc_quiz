from django.urls import path
from .views import index_view, get_next_question


app_name = "quiz"

urlpatterns = [
    path('', index_view, name='index'),
    path('get_next_question/<uuid:quiz_id>/', get_next_question, name='get_next_question'),
    # path('f/<slug:slug>/', download_file_view, name='download_file'),
    # path('<slug:slug>/', resolve_slug_view, name='resolve_slug'),
]