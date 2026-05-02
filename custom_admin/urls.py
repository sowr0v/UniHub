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
]
