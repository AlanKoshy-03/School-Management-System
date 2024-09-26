# forms.py
from django import forms
from .models import Student, Teacher, Class, Attendance

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['firstname', 'lastname', 'birthdate', 'gender', 'class_name']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['firstname', 'lastname', 'subject']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['classname', 'teacherid']  # List the fields you want to include in the form
        widgets = {
            'teacherid': forms.Select(),  # If you have a ForeignKey field
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['studentid', 'attendancedate', 'status']  # Removed 'classid'