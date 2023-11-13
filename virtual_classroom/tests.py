from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Classroom, Question

User = get_user_model()


class VirtualClassroomTestCase(APITestCase):

    def setUp(self):
        # Create test users
        self.teacher = User.objects.create_user(username='teacher', password='password', role='teacher')
        self.student = User.objects.create_user(username='student', password='password', role='student')
        self.other_teacher = User.objects.create_user(username='other-teacher', password='password', role='teacher')

        # Create a classroom
        self.classroom = Classroom.objects.create(title='class', teacher=self.teacher)
        self.classroom.enrolled_students.add(self.student)

    def login_and_get_token(self, username, password):
        url = reverse('login')
        data = {
            'username': username,
            'password': password
        }
        response = self.client.post(url, data)
        return response.data['token']

    def enroll_students(self, teacher_token, student_ids):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + teacher_token)
        url = reverse('add-students-to-classroom', args=[self.classroom.id])
        data = {'student_ids': student_ids}
        response = self.client.post(url, data)
        return response

    # Test User Registration
    def test_registration(self):
        url = reverse('signup')
        data = {'username': 'teacher', 'password': 'password', 'role': 'teacher'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test user login
    def test_login(self):
        url = reverse('login')
        data = {'username': 'student', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    # Test Classroom Creation
    def test_classroom_creation(self):
        token = self.login_and_get_token('teacher', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        url = reverse('create-classroom')
        data = {'title': 'new-class'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test enrolling students in own classroom
    def test_enroll_student(self):
        token = self.login_and_get_token('teacher', 'password')
        response = self.enroll_students(token, [self.student.id])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test enrolling students in other teacher's classroom
    def test_enroll_student_in_other_teacher_classroom(self):
        token = self.login_and_get_token('other-teacher', 'password')
        response = self.enroll_students(token, [self.student.id])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test Posting Questions in enrolled classroom
    def test_post_question_in_classroom(self):
        token = self.login_and_get_token('student', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        url = reverse('post-question', args=[self.classroom.id])
        data = {'text': "Can you explain this further?"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test Posting Questions in a not enrolled classroom
    def test_post_question_in_not_enrolled_classroom(self):
        token = self.login_and_get_token('student', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        another_classroom = Classroom.objects.create(title='new-class', teacher=self.other_teacher)
        url = reverse('post-question', args=[another_classroom.id])
        data = {'text': 'Can I ask a question here?'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test getting questions posted in a classroom
    def test_get_classroom_questions(self):
        url = reverse('get-questions', args=[self.classroom.id])
        question = Question.objects.create(text="What is this?", student=self.student, classroom=self.classroom)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expecting 1 question
        self.assertEqual(response.data[0]['text'], "What is this?")
