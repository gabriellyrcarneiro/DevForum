from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cadastro/", views.register, name="register"),
    path("pergunta/nova/", views.QuestionCreateView.as_view(), name="question_create"),
    path("pergunta/<int:pk>/", views.question_detail, name="question_detail"),
    path("pergunta/<int:pk>/editar/", views.QuestionUpdateView.as_view(), name="question_update"),
    path("pergunta/<int:pk>/excluir/", views.QuestionDeleteView.as_view(), name="question_delete"),
    path("pergunta/<int:pk>/curtir/", views.toggle_question_like, name="question_like"),
    path("resposta/<int:pk>/curtir/", views.toggle_answer_like, name="answer_like"),
    path("resposta/<int:pk>/melhor/", views.mark_best_answer, name="mark_best_answer"),
]