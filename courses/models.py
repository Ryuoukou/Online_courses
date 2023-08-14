import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    RUSSIAN_CITIES = (
        ("moscow", "Москва"),
        ("saint_petersburg", "Санкт-Петербург"),
        ("novosibirsk", "Новосибирск"),
        ("rostov_on_don", "Ростов-на-Дону"),
        ("samara", "Самара"),
        ("omsk", "Омск"),
        ("chelyabinsk", "Челябинск"),
        ("kazan", "Казань"),
        ("nizhny_novgorod", "Нижний Новгород"),
        ("ekaterinburg", "Екатеринбург"),
    )

    is_instructor = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(default=datetime.date(2000, 1, 1))
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\{9,15}$',
        message="Номер должен состоять только из цифр (от 9 до 15 цифр)"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, choices=RUSSIAN_CITIES, blank=True)
    GENDER_CHOICES = (
        ('М', 'Мужчина'),
        ('Ж', 'Женщина'),
        ('Д', 'Другое'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='Д')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        default_related_name = 'custom_users'


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_lessons(self):
        return Lesson.objects.filter(course=self)


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lesson')
    content = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Material(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_material')
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progresses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    completed_lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return f"{self.user} - {self.course}"
