from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import UserRegisterForm, QuestionForm, AnswerForm
from .models import Category, Question, Answer


def home(request):
    search = request.GET.get("q", "")
    category_slug = request.GET.get("categoria", "")

    questions = (
        Question.objects.select_related("author", "category")
        .annotate(answer_count=Count("answers"))
        .all()
    )

    if search:
        questions = questions.filter(
            Q(title__icontains=search)
            | Q(body__icontains=search)
            | Q(author__username__icontains=search)
        )

    if category_slug:
        questions = questions.filter(category__slug=category_slug)

    categories = Category.objects.all()

    context = {
        "questions": questions,
        "categories": categories,
        "search": search,
        "category_slug": category_slug,
    }

    return render(request, "forum/home.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta criada com sucesso! Bem-vindo ao DevForum.")
            return redirect("home")
    else:
        form = UserRegisterForm()

    return render(request, "registration/register.html", {"form": form})


def question_detail(request, pk):
    question = get_object_or_404(
        Question.objects.select_related("author", "category"),
        pk=pk,
    )

    answers = question.answers.select_related("author").all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "Você precisa fazer login para responder.")
            return redirect("login")

        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            messages.success(request, "Resposta publicada com sucesso!")
            return redirect("question_detail", pk=question.pk)
    else:
        form = AnswerForm()

    context = {
        "question": question,
        "answers": answers,
        "form": form,
    }

    return render(request, "forum/question_detail.html", context)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "forum/question_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Pergunta criada com sucesso!")
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "forum/question_form.html"

    def test_func(self):
        question = self.get_object()
        return question.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Pergunta atualizada com sucesso!")
        return super().form_valid(form)


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = "forum/question_confirm_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        question = self.get_object()
        return question.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Pergunta excluída com sucesso!")
        return super().form_valid(form)


@login_required
def toggle_question_like(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if question.likes.filter(pk=request.user.pk).exists():
        question.likes.remove(request.user)
        messages.info(request, "Curtida removida.")
    else:
        question.likes.add(request.user)
        messages.success(request, "Pergunta curtida!")

    return redirect("question_detail", pk=question.pk)


@login_required
def toggle_answer_like(request, pk):
    answer = get_object_or_404(Answer, pk=pk)

    if answer.likes.filter(pk=request.user.pk).exists():
        answer.likes.remove(request.user)
        messages.info(request, "Curtida removida.")
    else:
        answer.likes.add(request.user)
        messages.success(request, "Resposta curtida!")

    return redirect("question_detail", pk=answer.question.pk)


@login_required
def mark_best_answer(request, pk):
    answer = get_object_or_404(Answer.objects.select_related("question"), pk=pk)
    question = answer.question

    if question.author != request.user:
        messages.error(request, "Apenas o autor da pergunta pode marcar a melhor resposta.")
        return redirect("question_detail", pk=question.pk)

    Answer.objects.filter(question=question).update(is_best=False)

    answer.is_best = True
    answer.save()

    question.is_solved = True
    question.save()

    messages.success(request, "Melhor resposta marcada com sucesso!")
    return redirect("question_detail", pk=question.pk)