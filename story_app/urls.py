from django.urls import path 
from story_app import views



app_name = 'blog'


urlpatterns = [
    path('',views.index,name='index'),

]