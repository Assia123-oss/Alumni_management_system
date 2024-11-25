from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'alumni'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'), 
    path('profile/', views.ProfileView.as_view(), name='profile'), 
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('directory/', views.AlumniDirectoryView.as_view(), name='directory'),
    path('directory/<int:pk>/', views.AlumniDetailView.as_view(), name='alumni_detail'),
]