from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from .models import Course, Lesson
from .forms import CourseForm, RegistrationForm, LoginForm, LessonForm


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('courses:course_list')
    else:
        form = RegistrationForm()
    return render(request, 'courses/registration.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'courses/login.html'
    authentication_form = LoginForm


def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses:course_list')
    else:
        form = CourseForm

    return render(request, 'courses/create_course.html', {'form': form})


def create_lesson(request, course_id):
    course = Course.objects.get(pk=course_id)

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('courses:course_detail', course_id=course_id)
    else:
        form = LessonForm()

    return render(request, 'courses/create_lesson.html', {'form': form, 'course': course})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})


def lesson_detail(request, lesson_id, course_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})


def home_view(request):
    return render(request, 'courses/home.html')
