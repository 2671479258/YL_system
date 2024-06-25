from django.urls import path
from . import views
from utils.converters import UUIDConverter
from django.urls import register_converter

register_converter(UUIDConverter, 'uuid')



urlpatterns = [
    path('image_codes/<uuid:uuid>/', views.ImageCodeView.as_view())
]