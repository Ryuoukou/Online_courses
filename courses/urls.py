from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

app_name = 'courses'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('create_course/', views.create_course, name='create_course'),
    path('create_lesson/<int:course_id>/', views.create_lesson, name='create_lesson'),
    path('register/', views.registration_view, name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/', RedirectView.as_view(url='/'), name='profile_redirect'),
]