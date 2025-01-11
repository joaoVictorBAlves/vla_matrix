from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.models import User

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
