from django.urls import path
#Import the views file so that i can display something
from . import views
#Call the function i defined previously in views.py
urlpatterns = [
    #To actually display the views they need to be called to a URL
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]