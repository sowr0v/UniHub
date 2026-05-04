from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_university, name='add_university'),
    path('edit/<int:pk>/', views.edit_university, name='edit_university'),
    path('delete/<int:pk>/', views.delete_university, name='delete_university'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/delete/<int:user_id>/', views.delete_student, name='delete_student'),
    path('upload-csv/', views.upload_universities_csv, name='upload_csv'),
    path('clubs/', views.manage_clubs, name='manage_clubs'),
    path('clubs/add/', views.add_club, name='add_club'),
    path('clubs/edit/<int:pk>/', views.edit_club, name='edit_club'),
    path('clubs/delete/<int:pk>/', views.delete_club, name='delete_club'),
    path('admissions/', views.manage_admissions, name='manage_admissions'),
    path('admissions/add/', views.add_admission, name='add_admission'),
    path('admissions/edit/<int:pk>/', views.edit_admission, name='edit_admission'),
    path('admissions/delete/<int:pk>/', views.delete_admission, name='delete_admission'),
]
