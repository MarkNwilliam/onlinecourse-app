from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Choice, Submission


def index(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourse_app/index.html', {'courses': courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.all()
    context = {'course': course, 'lessons': lessons}
    return render(request, 'onlinecourse_app/course_details_bootstrap.html', context)


def lesson_details(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    questions = lesson.questions.all()
    context = {'lesson': lesson, 'questions': questions}
    return render(request, 'onlinecourse_app/lesson_details_bootstrap.html', context)


@login_required
def submit(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.method == 'POST':
        selected_choices = []
        for key in request.POST:
            if key.startswith('choice_'):
                choice_id = request.POST[key]
                try:
                    choice = Choice.objects.get(pk=choice_id)
                    selected_choices.append(choice)
                except Choice.DoesNotExist:
                    pass
        submission = Submission.objects.create(lesson=lesson, user=request.user)
        submission.choices.set(selected_choices)
        submission.save()
        return HttpResponseRedirect(reverse('onlinecourse_app:show_exam_result', args=(submission.id,)))
    return HttpResponseRedirect(reverse('onlinecourse_app:lesson_details', args=(lesson_id,)))


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    lesson = submission.lesson
    questions = lesson.questions.all()
    total_grade = sum(q.grade for q in questions)
    earned_grade = 0
    results = []
    for question in questions:
        correct_choices = question.choices.filter(is_correct=True)
        selected_choices = submission.choices.filter(question=question)
        if set(correct_choices) == set(selected_choices):
            earned_grade += question.grade
            results.append({'question': question, 'is_correct': True})
        else:
            results.append({'question': question, 'is_correct': False})
    context = {
        'submission': submission,
        'lesson': lesson,
        'total_grade': total_grade,
        'earned_grade': earned_grade,
        'results': results,
    }
    return render(request, 'onlinecourse_app/exam_result_bootstrap.html', context)
