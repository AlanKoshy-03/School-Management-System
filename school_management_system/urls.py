from django.contrib import admin
from django.urls import path, include
from school import views  # Import your views here

urlpatterns = [
    path('', views.home, name='home'),  # Root path mapped to home view
    path('admin/', admin.site.urls),
    path('students/', include('school.urls')),    # Your students URL configuration
    path('add/', views.add_student, name='add_student'),
    path('update/<str:student_id>/', views.update_student, name='update_student'),
    path('delete/<str:student_id>/', views.delete_student, name='delete_student'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:teacherid>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:teacherid>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:teacherid>/delete/', views.teacher_delete, name='teacher_delete'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/<int:classid>/update/', views.class_update, name='class_update'),
    path('classes/<int:classid>/delete/', views.class_confirm_delete, name='class_confirm_delete'),
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/add/', views.enrollment_add, name='enrollment_add'),
    path('enrollments/update/<int:enrollmentid>/', views.enrollment_update, name='enrollment_update'),
    path('enrollments/delete/<int:enrollmentid>/', views.enrollment_delete, name='enrollment_delete'),
    path('attendances/', views.attendance_list, name='attendance_list'),
    path('attendances/add/', views.attendance_add, name='attendance_add'),
    path('attendances/update/<int:attendanceid>/', views.attendance_update, name='attendance_update'),
    path('attendances/delete/<int:attendanceid>/', views.attendance_delete, name='attendance_delete'),
    path('attendance/statistics/', views.attendance_statistics, name='attendance_statistics'),
    path('attendance/select_student/', views.select_student_for_attendance, name='select_student_for_attendance'),
    path('comments/', views.comments_list, name='comments_list'),
    # path('attendance/select/', views.select_student_for_attendance, name='select_student_for_attendance'),
    # path('attendance/statistics/<int:student_id>/', attendance_statistics, name='student_attendance_statistics'),
]
