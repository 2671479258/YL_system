from django.urls import path
from . import views
urlpatterns = [
    path('adminlogin/',views.AdLogin.as_view()),



]
