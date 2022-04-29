from django.urls import URLPattern, path
from school import views

urlpatterns = [
    path('', views.home , name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('admission/<str:school_name>/', views.admission, name='admission'),
    path('admission_detail/<str:school_name>/<str:student>/', views.admission_detail, name='admission_detail'),
    path('student admission/<str:school_name>/<str:student>/', views.stud_admission, name='stud_admission'),
    path('register_admission/<str:school_name>/<str:student>/', views.register_admission, name='register_admission'),
    path('add_an_admission/<str:school_name>/<str:student>/', views.add_admission, name='add_admission'),
    path('accept_admission/<str:pk>/', views.accept_admission, name='accept_admission'),
    path('refuse_admission/<str:pk>/', views.refuse_admission, name='refuse_admission'),
    path('add_school_image/<str:school>/', views.add_school_image, name='add_school_image'),
    path('delete_school_picture/<str:pk>/', views.delete_school_picture, name='delete_school_picture'),
    path('student_class/<str:schoolname>/', views.school_classes, name='school_classes'),
    path('students/<str:schoolname>/<str:classe>/', views.students, name='students'),
    path('payment/<str:schoolname>/', views.payment, name='payments'),
    path('<str:school_name>/', views.school_page, name='school_page'),
]