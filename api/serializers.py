from rest_framework import serializers
from .models import Exam, Question, Item, Class, Student, Assessment

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name']  

class QuestionSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)  # Serializar os itens da questão

    class Meta:
        model = Question
        fields = ['id', 'title', 'items', 'correct']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)  # Serializando as questões dentro do exame

    class Meta:
        model = Exam
        fields = ['id', 'title', 'skills', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        exam = Exam.objects.create(**validated_data)

        for question_data in questions_data:
            items_data = question_data.pop('items')
            question = Question.objects.create(exam=exam, **question_data)
            for item_data in items_data:
                Item.objects.create(question=question, **item_data)
            exam.questions.add(question)  # Associa a questão ao exame

        return exam

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name']

class ClassSerializer(serializers.ModelSerializer):
    # Usando PrimaryKeyRelatedField para associar os alunos pela lista de IDs
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'students']

    def create(self, validated_data):
        students_data = validated_data.pop('students')
        new_class = Class.objects.create(**validated_data)
        
        # Associar os alunos pela lista de IDs
        for student in students_data:
            new_class.students.add(student)

        return new_class

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['student', 'exam', 'responses', 'result']
        
