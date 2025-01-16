import csv
from django.http import HttpResponse
from .models import Student, Exam, Question, Assessment, Class  

import csv
from django.http import HttpResponse
from .models import Student, Exam, Question, Assessment, Class  

def dynamic_generate_exam_results_csv(request, class_id=None, exam_id=None):
    # Recuperando a turma e o exame com base nos IDs fornecidos
    if exam_id:
        try:
            exam = Exam.objects.get(id=exam_id)  # Recuperando a prova com o id fornecido
        except Exam.DoesNotExist:
            return HttpResponse(f"Exame com id {exam_id} não encontrado", status=404)
        questions = Question.objects.filter(exam=exam)
    else:
        questions = None

    if class_id:
        try:
            students = Student.objects.filter(classes__id=class_id)  # Recupera os alunos da turma
        except Class.DoesNotExist:
            return HttpResponse(f"Turma com id {class_id} não encontrada", status=404)
    else:
        students = None

    # Se não passar o class_id nem exam_id, retorna um erro.
    if not (class_id or exam_id):
        return HttpResponse("É necessário fornecer pelo menos o ID de uma turma ou de um exame.", status=400)

    # Gerando cabeçalhos
    header = []
    data = []

    if exam_id and class_id:
        # Alunos x habilidades do exame
        header.append('student_id')  # Cabeçalho com o ID do aluno
        header.extend([f"skill_{skill}" for skill in exam.skills])  # Adiciona habilidades como colunas

        for student in students:
            row = [student.id]  # ID do aluno
            assessment = Assessment.objects.filter(exam=exam, student=student).first()
            if assessment:
                for _ in exam.skills:
                    # Calculando a média para cada habilidade do aluno
                    correct = sum(1 for q in questions if assessment.result['details'].get(str(q.id), False)) / len(questions)
                    row.append(correct)
            else:
                row.extend([0] * len(exam.skills))  # Se não houver avaliação, assume-se 0 para as habilidades
            data.append(row)

    elif exam_id and not class_id:
        # Turmas x questões, mostrando a média por questão
        header.append('class_id')  # Cabeçalho com o ID da turma
        header.extend([f"q{question.id}" for question in questions])  # Adiciona as questões como colunas

        class_data = {}
        for student in students:
            assessment = Assessment.objects.filter(exam=exam, student=student).first()
            if assessment:
                for question in questions:
                    correct = 1 if assessment.result['details'].get(str(question.id), False) else 0
                    if question.id not in class_data:
                        class_data[question.id] = []
                    class_data[question.id].append(correct)

        # Preenchendo os dados por turma
        for question in questions:
            row = [class_id]
            question_data = class_data.get(question.id, [])
            row.append(sum(question_data) / len(question_data) if question_data else 0)
            data.append(row)

    elif class_id and not exam_id:
        # Alunos x exames, mostrando a média dos alunos em cada exame
        header.append('student_id')  # Cabeçalho com o ID do aluno
        exams = Exam.objects.filter(classes__id=class_id)
        header.extend([f"exam_{exam.id}" for exam in exams])  # Adiciona os exames como colunas

        for student in students:
            row = [student.id]  # ID do aluno
            for exam in exams:
                assessment = Assessment.objects.filter(exam=exam, student=student).first()
                if assessment:
                    # Calculando a média do aluno no exame
                    correct = sum(1 for q in questions if assessment.result['details'].get(str(q.id), False)) / len(questions)
                    row.append(correct)
                else:
                    row.append(0)  # Se não houver avaliação, assume-se 0
            data.append(row)

    # Gerando o CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exam_results.csv"'
    writer = csv.writer(response)
    writer.writerow(header)  # Cabeçalho
    for row in data:
        writer.writerow(row)  # Dados dos alunos

    return response


def generate_exam_results_csv(request, class_id, exam_id):
    # Recuperando a turma e o exame com base nos IDs fornecidos
    try:
        exam = Exam.objects.get(id=exam_id)  # Recuperando a prova com o id fornecido
    except Exam.DoesNotExist:
        return HttpResponse(f"Exame com id {exam_id} não encontrado", status=404)
    
    try:
        students = Student.objects.filter(classes__id=class_id)  # Recupera os alunos da turma
    except Class.DoesNotExist:
        return HttpResponse(f"Turma com id {class_id} não encontrada", status=404)

    # Recuperando todas as questões do exame
    questions = Question.objects.filter(exam=exam)

    # Recuperando as respostas dos alunos para a prova específica
    assessments = Assessment.objects.filter(exam=exam, student__in=students)

    # Preparando os dados para a matriz
    header = ['student_id']  # Cabeçalho com o ID do aluno
    header.extend([f"q{question.id}" for question in questions])  # Adiciona as questões como colunas

    data = []

    # Preenchendo os dados para cada aluno
    for student in students:
        row = [student.id]  # ID do aluno
        for question in questions:
            # Verificando se o aluno acertou a questão
            assessment = assessments.filter(student_id=student.id).first()
            if assessment:
                correct = 1 if assessment.result['details'].get(str(question.id), False) else 0
            else:
                correct = 0
            row.append(correct)
        data.append(row)

    # Gerando o CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exam_results.csv"'
    writer = csv.writer(response)
    writer.writerow(header)  # Cabeçalho
    for row in data:
        writer.writerow(row)  # Dados dos alunos

    return response
