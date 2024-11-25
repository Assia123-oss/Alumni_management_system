from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('create/', views.EventCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='delete'),
    path('<int:pk>/participate/', views.EventParticipationView.as_view(), name='participate'),
    path('<int:pk>/cancel/', views.EventParticipationCancelView.as_view(), name='cancel'),
]