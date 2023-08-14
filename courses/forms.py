import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Course, User, Lesson
from django.forms.widgets import SelectDateWidget
from datetime import datetime


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    role = forms.ChoiceField(choices=(('student', 'Студент'), ('instructor', 'Преподаватель')))
    birth_date = forms.DateField(
        widget=SelectDateWidget(
            years=range(1900, datetime.now().year + 1),
            months={
                1: 'Январь',
                2: 'Февраль',
                3: 'Март',
                4: 'Апрель',
                5: 'Май',
                6: 'Июнь',
                7: 'Июль',
                8: 'Август',
                9: 'Сентябрь',
                10: 'Октябрь',
                11: 'Ноябрь',
                12: 'Декабрь',
            },
            empty_label=("Выберите год", "Выберите месяц", "Выберите день"),
        )
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'birth_date', 'gender', 'city', 'avatar']

    def sav(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')

        if role == 'student':
            user.is_instructor = False
        elif role == 'instructor':
            user.is_instructor = True

        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'instructor']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'order']
