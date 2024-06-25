from django.urls import path
from . import views

urlpatterns = [
    path('orders/settlement/', views.OrderSettlementView.as_view()),
    path('orders/commit/', views.OrderCommitView.as_view()),
path('personal-order/', views.PersonalOrder.as_view()),
path('TjA_test/',views.TjA_test.as_view())


]
