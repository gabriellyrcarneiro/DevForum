from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField("Título", max_length=200)
    body = models.TextField("Descrição")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Autor",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questions",
        verbose_name="Categoria",
    )
    likes = models.ManyToManyField(
        User,
        related_name="liked_questions",
        blank=True,
        verbose_name="Curtidas",
    )
    is_solved = models.BooleanField("Resolvida?", default=False)
    created_at = models.DateTimeField("Criada em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizada em", auto_now=True)

    class Meta:
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})

    def total_likes(self):
        return self.likes.count()


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Pergunta",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Autor",
    )
    body = models.TextField("Resposta")
    likes = models.ManyToManyField(
        User,
        related_name="liked_answers",
        blank=True,
        verbose_name="Curtidas",
    )
    is_best = models.BooleanField("Melhor resposta?", default=False)
    created_at = models.DateTimeField("Criada em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizada em", auto_now=True)

    class Meta:
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"
        ordering = ["-is_best", "-created_at"]

    def __str__(self):
        return f"Resposta de {self.author.username} em {self.question.title}"

    def total_likes(self):
        return self.likes.count()