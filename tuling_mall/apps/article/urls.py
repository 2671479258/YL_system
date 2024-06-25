from . import views
from django.urls import path
urlpatterns = [
    path('new_article/',views.new_article.as_view()),
    path('article/<article_id>',views.article_content.as_view()),
    path('yangsheng_article/',views.yangsheng_article.as_view()),
path('kepu_article/',views.kepu_article.as_view()),
    path('huli_article/',views.huli_article.as_view()),
    path('ALL_YS/',views.ALL_YS_article.as_view()),
path('ALL_KP/',views.ALL_KP_article.as_view()),
path('ALL_HL/',views.ALL_HL_article.as_view()),
path('user_search_article/', views.UserSearchArticle.as_view()),
    ]