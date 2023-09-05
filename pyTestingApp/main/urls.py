from django.urls import path
from . import views
from courses import views as courses_views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),
    path('courses/', courses_views.courses_show, name='app-courses'),
]