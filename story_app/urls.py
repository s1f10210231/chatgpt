from django.urls import path 
from story_app import views



app_name = 'story_app'


urlpatterns = [
    path('',views.index,name='index'),
    path('create/',views.create,name='create'),

]