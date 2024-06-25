from django.urls import path
from medicine import views
urlpatterns = [
path('index/', views.IndexView.as_view()),
    path('list/<category_id>/skus/', views.ListView.as_view()),
    path('hot/<category_id>/', views.HotGoodsView.as_view()),
    # path('search/', views.SKUSearchView()),

    path('detail/<sku_id>/', views.DetailView.as_view()),
path('search/', views.SearchView.as_view()),
]