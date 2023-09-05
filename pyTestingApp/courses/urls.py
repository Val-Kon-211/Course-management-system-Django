from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('course-create/', views.course_create, name='course-create'),
    path('course/<int:course_id>', views.course_open, name='course-open'),
    path('course/<int:course_id>/course-edit/', views.course_edit, name='course-edit'),
    path('course/<int:course_id>', views.course_delete, name='course-delete'),
    path('course/<int:course_id>/lesson-create/', views.lesson_create, name='lesson-create'),
    path('course/<int:course_id>/<int:lesson_id>/', views.lesson_theory, name='lesson-open'),
    path('course/<int:course_id>/<int:lesson_id>/lesson-edit', views.lesson_edit, name='lesson-edit'),
    path('course/<int:course_id>/<int:lesson_id>/', views.lesson_delete, name='lesson-delete'),
    path('course/<int:course_id>/', views.back_to_course, name='back-to-course'),
    path('course/<int:course_id>/<int:lesson_id>/theory', views.lesson_theory, name='theory'),
    path('course/<int:course_id>/<int:lesson_id>/task', views.lesson_task, name='task'),
    path('course/<int:course_id>/<int:lesson_id>/practice', views.lesson_practice, name='practice'),
    path('course/<int:course_id>/<int:lesson_id>/practice/runcode', views.runcode, name='runcode'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)