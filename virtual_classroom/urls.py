from django.urls import path
from .views import post_question, get_questions, signup, login, create_classroom, add_to_classroom

urlpatterns = [
    path('classrooms/<str:classroom_id>/questions', get_questions, name='get_questions'),
    path('classrooms/<str:classroom_id>/questions', post_question, name='post_question'),
    path('signup', signup),
    path('login', login),
    path('classrooms/create', create_classroom, name='create-classroom'),
    path('classrooms/<str:classroom_id>/add_students', add_to_classroom, name='add-students-to-classroom'),
]
