from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Question(models.Model):
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    choices = models.ManyToManyField(Choice)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
