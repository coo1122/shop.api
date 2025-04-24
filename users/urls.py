from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.RegisterAPIView),
    path('authorization/', views.AuthAPIView),
    path('confirm/', views.ConfirmAPIView),
]