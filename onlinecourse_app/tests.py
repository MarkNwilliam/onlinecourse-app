from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course, Lesson, Question, Choice, Submission


class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name="Python Basics",
            description="Learn Python from scratch"
        )

    def test_course_creation(self):
        self.assertEqual(self.course.name, "Python Basics")
        self.assertEqual(str(self.course), "Python Basics")

    def test_course_str_method(self):
        self.assertEqual(str(self.course), "Python Basics")


class LessonModelTest(TestCase):
    def setUp(self):
        course = Course.objects.create(name="Test Course", description="Test")
        self.lesson = Lesson.objects.create(
            title="Variables",
            content="Learning variables",
            course=course,
            order=1
        )

    def test_lesson_creation(self):
        self.assertEqual(self.lesson.title, "Variables")
        self.assertEqual(str(self.lesson), "Variables")


class QuestionModelTest(TestCase):
    def setUp(self):
        course = Course.objects.create(name="Test Course", description="Test")
        lesson = Lesson.objects.create(
            title="Test Lesson", content="Content", course=course, order=1
        )
        self.question = Question.objects.create(
            question_text="What is 2+2?",
            grade=2,
            lesson=lesson
        )

    def test_question_creation(self):
        self.assertEqual(self.question.question_text, "What is 2+2?")
        self.assertEqual(self.question.grade, 2)
        self.assertEqual(str(self.question), "What is 2+2?")


class ChoiceModelTest(TestCase):
    def setUp(self):
        course = Course.objects.create(name="Test Course", description="Test")
        lesson = Lesson.objects.create(
            title="Test Lesson", content="Content", course=course, order=1
        )
        question = Question.objects.create(
            question_text="What is 2+2?", grade=2, lesson=lesson
        )
        self.choice = Choice.objects.create(
            choice_text="4",
            is_correct=True,
            question=question
        )

    def test_choice_creation(self):
        self.assertTrue(self.choice.is_correct)
        self.assertEqual(str(self.choice), "4")


class SubmissionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        course = Course.objects.create(name="Test Course", description="Test")
        self.lesson = Lesson.objects.create(
            title="Test Lesson", content="Content", course=course, order=1
        )
        self.submission = Submission.objects.create(
            lesson=self.lesson,
            user=self.user
        )

    def test_submission_creation(self):
        self.assertEqual(self.submission.user.username, "testuser")
        self.assertIsNotNone(self.submission.submitted_at)
