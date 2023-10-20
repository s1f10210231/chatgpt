from django.urls import path 
from story_app import views



app_name = 'story_app'


urlpatterns = [
    path('',views.index,name='index'),
    path('create/',views.create,name='create'),
    path('browse/',views.browse,name='browse'),
    path('<int:novel_id>/detail/', views.detail, name='detail'),
    path('<int:novel_id>/like/', views.like, name='like'),
    path('genre/<str:genre>/',views.genre_page,name='genre_page'),
    path('time_page/',views.time_page,name='time_page')
]