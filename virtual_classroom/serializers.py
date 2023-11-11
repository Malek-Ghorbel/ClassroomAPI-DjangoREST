from rest_framework import serializers
from .models import Classroom, Question, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'password']

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        # Remove password from the representation
        representation.pop('password', None)
        return representation


class ClassroomSerializer(serializers.ModelSerializer):
    enrolled_students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'title', 'teacher', 'enrolled_students']
        extra_kwargs = {'teacher': {'read_only': True}}


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'student', 'classroom', 'timestamp']
        read_only_fields = ('student', 'classroom', 'timestamp')
