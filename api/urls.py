from django.urls import path
from .heatmap import generate_exam_results_csv, dynamic_generate_exam_results_csv
from .views import LoginView, RegisterView, ExamView, QuestionView, StudentListView, StudentCreateView, ClassListView, ClassCreateView, AssessmentCreateView, ExamListView, AssessmentDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('exams/', ExamListView.as_view(), name='create_exam'),
    path('exams/<int:exam_id>/', ExamView.as_view(), name='get_exam'),
    path('exams/<int:exam_id>/questions/<int:question_id>/', QuestionView.as_view(), name='get_question'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/create/', StudentCreateView.as_view(), name='student-create'),
    path('classes/', ClassListView.as_view(), name='class-list'),
    path('classes/create/', ClassCreateView.as_view(), name='class-create'),
    path('assessments/create/', AssessmentCreateView.as_view(), name='create-assessment'),
    path('assessment/<uuid:student_id>/<int:exam_id>/', AssessmentDetailView.as_view(), name='assessment-detail'),
    path('assessments/heatmap/<uuid:class_id>/<int:exam_id>/',              generate_exam_results_csv, name='generate_heatmap'),
    path('assessments/heatmap/skills/<uuid:class_id>/<int:exam_id>/',              dynamic_generate_exam_results_csv, name='generate_heatmap_skills'),
    path('assessments/heatmap/<uuid:class_id>/', dynamic_generate_exam_results_csv, name='generate_class_results'),
    path('assessments/heatmap/<int:exam_id>/', dynamic_generate_exam_results_csv, name='generate_exam_results'),
]
