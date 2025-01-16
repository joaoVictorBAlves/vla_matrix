from django.db import models
import uuid

class Exam(models.Model):
    title = models.CharField(max_length=100)
    skills = models.JSONField()
    # Alterando o related_name para evitar conflito
    questions = models.ManyToManyField('Question', related_name='exams')

    def __str__(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=255)
    skill = models.CharField(max_length=100)
    correct = models.CharField(max_length=100) 
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions_related')

    def __str__(self):
        return self.title


class Item(models.Model):
    question = models.ForeignKey(Question, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Class(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(Student, related_name='classes')

    def __str__(self):
        return self.name

class Assessment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    responses = models.JSONField()  
    result = models.JSONField(null=True, blank=True) 

    def __str__(self):
        return f'Assessment for {self.student.name} in {self.exam.title}'

class Answer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()  # True se a resposta estiver correta, False caso contrário

class StudentExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    grade = models.FloatField()  # Nota final do aluno na prova