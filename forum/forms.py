from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Question, Answer


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite seu e-mail",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Usuário",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite seu nome de usuário",
                }
            ),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "category", "body"]
        labels = {
            "title": "Título da pergunta",
            "category": "Categoria",
            "body": "Descrição da dúvida",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Como fazer login no Django?",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 7,
                    "placeholder": "Explique sua dúvida com detalhes...",
                }
            ),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["body"]
        labels = {
            "body": "Sua resposta",
        }
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Escreva uma resposta clara e objetiva...",
                }
            ),
        }