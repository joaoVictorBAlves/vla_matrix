from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import ExamSerializer, QuestionSerializer, StudentSerializer, ClassSerializer, AssessmentSerializer
from .models import Exam, Question, Student, Class, Assessment

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Extraindo os parâmetros username e password da requisição
        username = request.data.get('username')
        password = request.data.get('password')

        # Verificar se username e password foram fornecidos
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Autenticação do usuário
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Extraindo os parâmetros do request
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Verificando se os parâmetros necessários estão presentes
        if not username or not email or not password:
            return Response({'error': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar se o nome de usuário já está em uso
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar se o e-mail já está em uso
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # Criar o novo usuário
        user = User.objects.create_user(username=username, email=email, password=password)

        # Gerar o token para o novo usuário
        token, created = Token.objects.get_or_create(user=user)

        # Retornar o token de autenticação
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class ExamView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            exam = serializer.save()
            return Response({"message": "Exam created successfully", "exam_id": exam.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, exam_id, *args, **kwargs):
        try:
            exam = Exam.objects.get(id=exam_id)
            serializer = ExamSerializer(exam)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, exam_id, *args, **kwargs):
        try:
            exam = Exam.objects.get(id=exam_id)
            exam.delete()
            return Response({"message": "Exam deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

class ExamListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        exams = Exam.objects.all()
        exam_list = [{"id": exam.id, "title": exam.title, "skills": exam.skills} for exam in exams]
        return Response(exam_list, status=status.HTTP_200_OK)

class QuestionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, exam_id, question_id, *args, **kwargs):
        try:
            exam = Exam.objects.get(id=exam_id)
            question = Question.objects.get(id=question_id, exam=exam)
            
            serializer = QuestionSerializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)
        
# View para cadastrar alunos
class StudentCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View para listar alunos
class StudentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

# View para cadastrar turmas
class ClassCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View para listar turmas
class ClassListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AssessmentCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Validar os dados enviados para o cadastro do Assessment
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            # Criar o Assessment sem o resultado
            assessment = serializer.save()
            exam = assessment.exam
            
            # Validar que o exame tem questões associadas
            if not exam.questions.exists():
                return Response(
                    {"error": "The selected exam has no questions associated."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            correct_answers = {}
            total_correct = 0

            # Comparar as respostas enviadas com as respostas corretas
            for question in exam.questions.all():
                question_id = str(question.id)
                student_response = assessment.responses.get(question_id)

                if student_response is not None:
                    
                    is_correct = student_response == question.correct
                    correct_answers[question_id] = is_correct

                    if is_correct:
                        total_correct += 1
                else:
                    correct_answers[question_id] = None  # Resposta ausente

            # Atualizar o resultado no modelo de Assessment
            assessment.result = {
                "details": correct_answers,
                "total_correct": total_correct,
                "total_questions": exam.questions.count(),
            }
            assessment.save()

            return Response(
                {
                    "message": "Assessment created successfully",
                    "assessment_id": assessment.id,
                    "result": assessment.result,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AssessmentDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, student_id, exam_id):
        try:
            student = Student.objects.get(id=student_id)
            exam = Exam.objects.get(id=exam_id)
            assessment = Assessment.objects.get(student=student, exam=exam)
            
            serializer = AssessmentSerializer(assessment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)
        except Assessment.DoesNotExist:
            return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)