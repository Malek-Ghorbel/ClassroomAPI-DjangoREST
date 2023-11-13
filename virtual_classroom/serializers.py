from rest_framework import serializers
from .models import Classroom, Question, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'password']


# Used for returning users we shall not return the password
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'role')


class ClassroomSerializer(serializers.ModelSerializer):
    enrolled_students = UserDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'title', 'teacher', 'enrolled_students']
        extra_kwargs = {'teacher': {'read_only': True}}


class EnrollStudentSerializer(serializers.Serializer):
    student_ids = serializers.ListField(
        child=serializers.IntegerField()
    )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'student_id', 'classroom_id', 'timestamp']
        read_only_fields = ('student', 'classroom', 'timestamp')
