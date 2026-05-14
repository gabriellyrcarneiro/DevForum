from django.contrib import admin
from .models import Category, Question, Answer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "is_solved", "created_at"]
    list_filter = ["category", "is_solved", "created_at"]
    search_fields = ["title", "body", "author__username"]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["question", "author", "is_best", "created_at"]
    list_filter = ["is_best", "created_at"]
    search_fields = ["body", "author__username", "question__title"]