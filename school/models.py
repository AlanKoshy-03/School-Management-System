from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]
    studentid = models.AutoField(primary_key=True, db_column='STUDENTID')
    firstname = models.CharField(max_length=50, db_column='FIRSTNAME')
    lastname = models.CharField(max_length=50, db_column='LASTNAME')
    birthdate = models.DateField(db_column='BIRTHDATE')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_column='GENDER')
    class_name = models.CharField(max_length=50, db_column='CLASS')

    class Meta:
        db_table = '"STUDENTS"'  # Note the double quotes and uppercase table name
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Teacher(models.Model):
    teacherid = models.AutoField(primary_key=True)  # AutoField for primary key
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50, null=True, blank=True)  # Nullable field
    subject = models.CharField(max_length=50)

    class Meta:
        db_table = 'teachers'  # Ensure the table name matches
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}" if self.lastname else self.firstname


class Class(models.Model):
    classid = models.AutoField(primary_key=True, db_column='CLASSID')
    classname = models.CharField(max_length=100, db_column='CLASSNAME')
    teacherid = models.ForeignKey('Teacher', on_delete=models.CASCADE, db_column='TEACHERID')  # Ensure this matches

    class Meta:
        db_table = 'CLASSES'
    
    def __str__(self):
        return self.classname

class Enrollment(models.Model):
    enrollmentid = models.AutoField(primary_key=True, db_column='ENROLLMENTID')
    studentid = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='STUDENTID')
    classid = models.ForeignKey('Class', on_delete=models.CASCADE, db_column='CLASSID')
    enrollmentdate = models.DateField(db_column='ENROLLMENTDATE')

    class Meta:
        db_table = 'ENROLLMENTS'  # Ensure the table name matches the exact name in your database
        unique_together = ('studentid', 'classid')
    
    def __str__(self):
        return f"{self.studentid} enrolled in {self.classid} on {self.enrollmentdate}" 

from django.db import models

class Attendance(models.Model):
    attendanceid = models.AutoField(primary_key=True)
    studentid = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='STUDENTID')  # Explicitly set the column name
    classid = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='CLASSID')  # Explicitly set the column name
    attendancedate = models.DateField()
    status = models.CharField(max_length=1)

    class Meta:
        db_table = 'attendance'
        
    def __str__(self):
        return f"Attendance for {self.studentid.firstname} {self.studentid.lastname} in {self.classid.classname} on {self.attendancedate}"

class Comments(models.Model):
    commentid = models.AutoField(primary_key=True)
    studentid = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='STUDENTID')  # Ensure Student is correctly referenced
    comment_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'

