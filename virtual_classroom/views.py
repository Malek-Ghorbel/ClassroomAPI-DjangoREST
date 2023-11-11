from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Classroom, Question, User, UserRole
from .serializers import QuestionSerializer, UserSerializer, ClassroomSerializer
from rest_framework.authtoken.models import Token


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


@api_view(['POST'])
def signup(request):
    # Serialize the user
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        # Save the password as hash
        user.set_password(request.data['password'])
        user.save()
        # Create the token and return it
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    # Get the user if it exists
    user = get_object_or_404(User, username=request.data['username'])

    # Check password
    if not user.check_password(request.data['password']):
        return Response("wrong password", status=status.HTTP_404_NOT_FOUND)

    # return the token
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key , 'user': serializer.data})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsTeacher])
def create_classroom(request):
    # Set the classroom teacher as the current user
    request.data['teacher'] = request.user.id

    # Create the classroom and save it
    serializer = ClassroomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(teacher=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsTeacher])
def add_to_classroom(request, classroom_id):
    # Get the classroom if exists
    classroom = get_object_or_404(Classroom, id=classroom_id)

    # Check if the request user is the teacher who owns the classroom
    if classroom.teacher != request.user:
        return Response({'error': 'Only the classroom teacher can add students.'}, status=status.HTTP_403_FORBIDDEN)

    # Get the student ids from the request
    student_ids = request.data.get('student_ids', [])

    # Filter the users who have these ids and are actually students
    students = User.objects.filter(id__in=student_ids, role=UserRole.STUDENT)

    # Enroll them in the classroom
    classroom.enrolled_students.add(*students)
    return Response({"message": "Students added successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsStudent])
def post_question(request, classroom_id):
    # Get the classroom if exists
    classroom = get_object_or_404(Classroom, id=classroom_id)

    # Check if user is enrolled
    if request.user not in classroom.enrolled_students.all():
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # Create the question and save it
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(student=request.user, classroom=classroom)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_questions(request, classroom_id):
    # Filter the question by classroom id and order by date
    questions = Question.objects.filter(classroom_id=classroom_id).order_by('-timestamp')
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)
