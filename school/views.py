# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Comments
from .forms import StudentForm
from django.db import IntegrityError
from django.db import connection
def home(request):
    return render(request, 'home.html')

# Students
def student_list(request):
    students = Student.objects.all()
    error_message = request.GET.get('error', '')  # Get error message from query parameters
    return render(request, 'students/student_list.html', {'students': students, 'error_message': error_message})

# View to add a new student
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})

# View to update a student
def update_student(request, student_id):
    student = get_object_or_404(Student, studentid=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Update Student'})

def delete_student(request, student_id):
    student = get_object_or_404(Student, studentid=student_id)
    if request.method == 'POST':
        try:
            student.delete()
            return redirect('student_list')  # Redirect to the student list view
        except IntegrityError:
            # Handle the exception if there are foreign key constraints
            return render(request, 'students/student_confirm_delete.html', {
                'student': student,
                'error_message': 'This student has associated records. Please delete or update those records before deleting this student.'
            })
    return render(request, 'students/student_confirm_delete.html', {'student': student})

# Teachers
from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher
from .forms import TeacherForm  # Assuming you have created a form for Teacher

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def teacher_detail(request, teacherid):
    teacher = get_object_or_404(Teacher, teacherid=teacherid)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})

def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'teachers/teacher_form.html', {'form': form})

def teacher_update(request, teacherid):
    teacher = get_object_or_404(Teacher, teacherid=teacherid)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/update_teacher.html', {'form': form})

def teacher_delete(request, teacherid):
    teacher = get_object_or_404(Teacher, teacherid=teacherid)
    if request.method == 'POST':
        try:
            teacher.delete()
            return redirect('teacher_list')
        except IntegrityError:
            # Handle the exception if there are foreign key constraints
            return render(request, 'teachers/teacher_confirm_delete.html', {
                'teacher': teacher,
                'error_message': 'This teacher has associated records. Please delete or update those records before deleting this teacher.'
            })
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': teacher})

# Classes
from django.shortcuts import render, get_object_or_404
from .models import Class
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ClassForm  

def class_list(request):
    classes = Class.objects.all()
    return render(request, 'classes/class_list.html', {'classes': classes})

def class_update(request, classid):
    cls = get_object_or_404(Class, classid=classid)

    if request.method == 'POST':
        form = ClassForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm(instance=cls)

    return render(request, 'classes/class_update.html', {'form': form, 'title': 'Update Class'})

def class_confirm_delete(request, classid):
    cls = get_object_or_404(Class, classid=classid)
    error_message = None
    
    if request.method == 'POST':
        try:
            cls.delete()
            messages.success(request, 'Class deleted successfully!')
            return redirect('class_list')  # Redirect to the class list view
        except IntegrityError:
            # This error occurs if there are related records in other tables
            error_message = 'This class has associated records. Please delete or update those records before deleting this class.'

    return render(request, 'classes/class_confirm_delete.html', {
        'class': cls, 
        'title': 'Confirm Delete',
        'error_message': error_message
    })

# Enrollments
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Enrollment, Student, Class

def enrollment_list(request):
    enrollments = Enrollment.objects.select_related('studentid', 'classid').all()
    return render(request, 'enrollments/enrollment_list.html', {'enrollments': enrollments})

def enrollment_add(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        class_id = request.POST.get('cls')
        enrollment_date = request.POST.get('enrollment_date')
        student = get_object_or_404(Student, pk=student_id)
        cls = get_object_or_404(Class, pk=class_id)

        try:
            enrollment = Enrollment.objects.create(student=student, cls=cls, enrollment_date=enrollment_date)
            messages.success(request, 'Enrollment added successfully!')
            return redirect('enrollment_list')
        except:
            messages.error(request, 'An error occurred while adding enrollment. Check for duplicate records.')
            return redirect('enrollment_add')

    students = Student.objects.all()
    classes = Class.objects.all()
    return render(request, 'enrollments/enrollment_form.html', {'students': students, 'classes': classes})

def enrollment_update(request, enrollmentid):
    enrollment = get_object_or_404(Enrollment, enrollmentid=enrollmentid)

    # Log the enrollment details for debugging
    print(f"Updating Enrollment ID: {enrollment.enrollmentid}")
    print(f"Current Student ID: {enrollment.studentid.studentid}")  # Assuming studentid is a foreign key
    print(f"Current Class ID: {enrollment.classid.classid}")  # Assuming classid is a foreign key

    if request.method == 'POST':
        enrollment_date = request.POST.get('enrollment_date')

        if enrollment_date:
            try:
                # Update the enrollment date
                enrollment.enrollmentdate = enrollment_date  # Ensure this matches your model
                enrollment.save()
                messages.success(request, 'Enrollment date updated successfully!')
                return redirect('enrollment_list')
            except Exception as e:
                messages.error(request, f'An error occurred while updating enrollment: {str(e)}')
                return redirect('enrollment_update', enrollmentid=enrollmentid)

    # Fetch the current student and class for display
    current_student = enrollment.studentid
    current_class = enrollment.classid

    return render(request, 'enrollments/enrollment_update_form.html', {
        'enrollment': enrollment,
        'enrollment_date': enrollment.enrollmentdate.strftime('%Y-%m-%d'),  # Ensure this field exists
        'current_student': current_student,  # Assuming this is a foreign key
        'current_class': current_class,  # Assuming this is a foreign key
    })

   

def enrollment_delete(request, enrollmentid):
    enrollment = get_object_or_404(Enrollment, enrollmentid=enrollmentid)

    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Enrollment deleted successfully!')
        return redirect('enrollment_list')

    return render(request, 'enrollments/enrollment_confirm_delete.html', {'enrollment': enrollment})
 
# Attendance
from django.shortcuts import render, redirect
from .models import Attendance

def attendance_list(request):
    attendances = Attendance.objects.all()
    print(attendances.query)  # Log the query
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

def attendance_add(request):
    students = Student.objects.all()  # Fetch all students

    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        attendancedate = request.POST.get('attendancedate')
        status = request.POST.get('status')

        if studentid and attendancedate and status:
            try:
                student_instance = Student.objects.get(studentid=studentid)
                
                # Automatically determine the class based on the selected student's class_name
                class_instance = Class.objects.get(classname=student_instance.class_name)
                
                # Create and save the new Attendance record
                Attendance.objects.create(
                    studentid=student_instance,
                    classid=class_instance,
                    attendancedate=attendancedate,
                    status=status
                )

                return redirect('attendance_list')  # Redirect to the attendance list page on success

            except Student.DoesNotExist:
                error_message = "Selected student does not exist."
            except Class.DoesNotExist:
                error_message = "Class associated with the student does not exist."
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
        else:
            error_message = "All fields are required."

        return render(request, 'attendance/attendance_add.html', {
            'students': students,
            'error_message': error_message
        })

    # Initial GET request, render the empty form
    return render(request, 'attendance/attendance_add.html', {
        'students': students
    })


def attendance_delete(request, attendanceid):
    attendance = Attendance.objects.get(pk=attendanceid)
    if request.method == 'POST':
        attendance.delete()
        return redirect('attendance_list')
    return render(request, 'attendance/attendance_confirm_delete.html', {'attendance': attendance})
from .forms import AttendanceForm  # Import the form
from datetime import datetime


def attendance_update(request, attendanceid):
    attendance = get_object_or_404(Attendance, pk=attendanceid)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            student = form.cleaned_data['studentid']  # Get the selected student
            # Automatically assign classid based on student's class
            try:
                class_instance = Class.objects.get(classname=student.class_name)
                form.instance.classid = class_instance
            except Class.DoesNotExist:
                form.add_error('studentid', 'Class for this student does not exist in the Class model.')
                return render(request, 'attendance/attendance_update.html', {
                    'form': form,
                    'attendance_details': f"Student: {attendance.studentid}, Date: {attendance.attendancedate}, Status: {attendance.status}",
                    'title': 'Update Attendance'
                })
            
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    
    return render(request, 'attendance/attendance_update.html', {
        'form': form,
        'attendance_details': f"Student: {attendance.studentid}, Date: {attendance.attendancedate}, Status: {attendance.status}",
        'title': 'Update Attendance'
    })

def attendance_statistics(request):
    total_attendance = Attendance.objects.count()
    present_count = Attendance.objects.filter(status='P').count()
    absent_count = Attendance.objects.filter(status='A').count()

    # Calculate attendance percentage
    if total_attendance > 0:
        attendance_percentage = (present_count / total_attendance) * 100
    else:
        attendance_percentage = 0

    context = {
        'total_attendance': total_attendance,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_percentage': attendance_percentage,
        'students': Student.objects.all(),  # Add this to get the student list
    }
    return render(request, 'attendance/attendance_statistics.html', context)


from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q

def select_student_for_attendance(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')

        if student_id:
            selected_student = get_object_or_404(Student, studentid=student_id)

            student_total_attendance = Attendance.objects.filter(studentid=student_id).count()
            student_present_count = Attendance.objects.filter(studentid=student_id, status='P').count()
            student_absent_count = Attendance.objects.filter(studentid=student_id, status='A').count()

            # Calculate attendance percentage
            if student_total_attendance > 0:
                attendance_percentage = (student_present_count / student_total_attendance) * 100
            else:
                attendance_percentage = None  # No attendance records

            context = {
                'selected_student': selected_student,
                'student_total_attendance': student_total_attendance,
                'student_present_count': student_present_count,
                'student_absent_count': student_absent_count,
                'attendance_percentage': attendance_percentage,
            }
            return render(request, 'attendance/select_student.html', context)
        else:
            error_message = "Please select a student."
            return render(request, 'attendance/attendance_statistics.html', {'error_message': error_message})

    return render(request, 'attendance/attendance_statistics.html')

def comments_list(request):
    comments = Comments.objects.select_related('studentid').all()  # Use select_related for better performance
    print(comments)
    return render(request, 'comments/comments_list.html', {'comments': comments})




