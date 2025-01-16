import random
import requests

# Lista de alunos previamente definida (IDs dos alunos)
students = [
    "dc0e40d4-b7c6-4170-b1c4-290aba2d306d",
    "a2a833a8-4bba-4995-b095-31c2a34a017e",
    "da2d7fa2-a320-461d-a835-cf11e200ef90",
    "8f6cf8b7-0427-400f-aaf3-d47af46dee4c",
    "f35d2d29-9ce8-4e65-a17c-fe2820b88519",
    "33a73703-3127-4815-a692-17edf8883ce0",
    "10c12070-f4e5-44ed-a6cf-8ee88fa178ab",
    "4473d87c-2da4-475c-adcc-1d2a22ab4ab1",
    "00620e0f-7f73-4e48-a171-4a47507a2bd5",
    "c844cc91-f455-49d7-bc0e-a865a401f5d3",
    "f33b1dd6-84e2-44b1-92a0-da60f83026e9",
    "a2307db6-ea9a-4621-9677-710b8c88054e",
    "ddda97fb-2599-4d7e-8cb2-6d286baa1852",
    "40ac3f7b-0e53-4304-a550-a5c033d54288",
    "021bd688-872e-41c4-8108-00ba9973d2d7",
    "4222f279-88c4-4152-b798-74697ad0ab6d",
    "c50af889-2b2b-462b-adb0-fa2b0631484d",
    "c699ee5f-4c15-46fe-8c9f-990d131f1a41",
    "97c11579-19c5-4e63-8b81-9c7c5d97fce1",
    "625ab708-2143-4a98-b6e0-2ce14c63a7d4"
]

# IDs dos exames
exams = [3]

# Endpoint para obter detalhes do exame
exam_endpoint = "http://127.0.0.1:8000/api/exams/{id}/"

# Endpoint para criar o assessment
create_assessment_endpoint = "http://127.0.0.1:8000/api/assessments/create/"

# Função para obter detalhes do exame
def get_exam_details(exam_id):
    url = exam_endpoint.format(id=exam_id)
    print(f"Obtendo detalhes do exame {exam_id} com URL {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Função para gerar respostas para um aluno com base na performance
def generate_responses(exam, performance):
    # Usar o ID da questão como chave para as respostas corretas
    correct_answers = {str(q["id"]): q["correct"] for q in exam["questions"]}
    questions = {str(q["id"]): [item["name"] for item in q["items"]] for q in exam["questions"]}

    responses = {}
    
    for question_id, options in questions.items():
        if performance == "good":
            chance = random.random()
            response = correct_answers[question_id] if chance <= 0.9 else random.choice(options)
        elif performance == "intermediate":
            chance = random.random()
            response = correct_answers[question_id] if chance <= 0.6 else random.choice(options)
        else:  # bad performance
            chance = random.random()
            response = correct_answers[question_id] if chance <= 0.3 else random.choice(options)

        responses[question_id] = response
    
    return responses

# Função para determinar a performance do aluno
def determine_performance():
    return random.choice(["good", "intermediate", "bad"])

# Função principal para criar assessments
def create_assessments():
    for student in students:
        for exam_id in exams:
            try:
                print(f"Iniciando criação de assessment para o aluno {student} no exame {exam_id}")
                
                # Obter detalhes do exame
                exam = get_exam_details(exam_id)
                print(f"Detalhes do exame obtidos: {exam}")

                # Determinar performance do aluno
                performance = determine_performance()
                print(f"Performance do aluno {student}: {performance}")

                # Gerar respostas do aluno
                responses = generate_responses(exam, performance)
                print(f"Respostas geradas para o aluno {student}: {responses}")

                # Criar o payload para o assessment
                payload = {
                    "student": student,
                    "exam": exam_id,
                    "responses": responses,
                }
                print(f"Payload criado: {payload}")

                # Enviar o assessment
                response = requests.post(create_assessment_endpoint, json=payload)
                response.raise_for_status()
                print(f"Assessment criado para o aluno {student} no exame {exam_id}.")
            except Exception as e:
                print(f"Erro ao criar assessment para o aluno {student} no exame {exam_id}: {e}")

# Executar o script
if __name__ == "__main__":
    create_assessments()
