from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    STUDENT = 'student', 'Student'
    TEACHER = 'teacher', 'Teacher'


# User model
class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
    )


# Classroom model
class Classroom(models.Model):
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey('User', on_delete=models.CASCADE, related_name='teacher_classrooms')
    enrolled_students = models.ManyToManyField(User, related_name='enrolled_classrooms')


# Question model
class Question(models.Model):
    text = models.TextField()
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='questions')
