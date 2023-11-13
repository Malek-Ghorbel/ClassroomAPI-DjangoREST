from django.urls import path
from .views import post_question, get_questions, signup, login, create_classroom, add_to_classroom

urlpatterns = [
    path('classroom/<str:classroom_id>/questions', get_questions, name='get-questions'),
    path('classroom/<str:classroom_id>/question', post_question, name='post-question'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('classroom/create', create_classroom, name='create-classroom'),
    path('classroom/<str:classroom_id>/add_students', add_to_classroom, name='add-students-to-classroom'),
]
