from django.db import models

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    type = models.CharField(max_length=20)

class Department(models.Model):
    dept_name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

class Course(models.Model):
    course_name = models.CharField(max_length=50)
    DEPARTMENT = models.ForeignKey(Department,on_delete=models.CASCADE)
    duration = models.CharField(max_length=10)

class Staff(models.Model):
    staff_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=30)
    staff_photo = models.CharField(max_length=30)
    staff_email = models.CharField(max_length=30)
    staff_phone = models.CharField(max_length=30)
    DEPARTMENT = models.ForeignKey(Department, on_delete=models.CASCADE)
    gender = models.CharField(max_length=30)
    staff_house = models.CharField(max_length=40)
    staff_location = models.CharField(max_length=50)
    staff_pincode = models.CharField(max_length=10)
    staff_dob = models.DateField()
    staff_education = models.CharField(max_length=200)
    staff_experience = models.CharField(max_length=200)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)

class Subject(models.Model):
    subject_name = models.CharField(max_length=30)
    COURSE = models.ForeignKey(Course,on_delete=models.CASCADE)
    sem = models.CharField(max_length=10)
    STAFF = models.ForeignKey(Staff,on_delete=models.CASCADE)

class Student(models.Model):
    student_name = models.CharField(max_length=30)
    student_photo = models.CharField(max_length=30)
    student_email = models.CharField(max_length=30)
    student_phone = models.CharField(max_length=30)
    DEPARTMENT = models.ForeignKey(Department, on_delete=models.CASCADE)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    sem = models.CharField(max_length=10)
    parent_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    student_house = models.CharField(max_length=40)
    student_location = models.CharField(max_length=40)
    student_pincode = models.CharField(max_length=10)
    student_dob = models.DateField()
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)

class Timetable(models.Model):
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    sem = models.CharField(max_length=30)
    SUBJECT_1 = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='sub_1')
    SUBJECT_2 = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='sub_2')
    SUBJECT_3 = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='sub_3')
    SUBJECT_4 = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='sub_4')
    SUBJECT_5 = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='sub_5')
    SUBJECT_6 = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='sub_6')
    Day = models.CharField(max_length=30)


class Attendance(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,default="")
    date = models.DateField()
    hour = models.CharField(max_length=20,default="")
    period = models.CharField(max_length=20,default='')
    SUBJECT = models.ForeignKey(Subject,on_delete=models.CASCADE)

class Leave(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=30)
    STAFF = models.ForeignKey(Staff ,on_delete=models.CASCADE)

class Feedback(models.Model):
    FROM = models.ForeignKey(Login, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)
    date = models.DateField()

class Chat(models.Model):
    FROM = models.ForeignKey(Login, on_delete=models.CASCADE,related_name="from_id")
    TO = models.ForeignKey(Login, on_delete=models.CASCADE,related_name='to_id')
    date = models.DateField()
    desc = models.CharField(max_length=100)



