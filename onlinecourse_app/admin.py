from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Course, Lesson, Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'grade', 'lesson']
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    inlines = [QuestionInline]


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'pub_date']
    inlines = [LessonInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
