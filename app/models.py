from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Customeruser(AbstractUser):
    USER =(
        (1,'owner'),
         (2,'staff'),
          (3,'student'),
    )

    user_type =models.CharField(choices=USER,max_length=50,default=1)
    profile_pic =models.ImageField(upload_to='media/profile_pic')
    # profile_pic =models.ImageField(upload_to='static/assets/img/profiles')

class course(models.Model):
    name =models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Session_Year(models.Model):
    session_start = models.CharField(max_length=100)
    session_end = models.CharField(max_length=100)
    def __str__(self):
        return self.session_start + " to " + self.session_end


# class student(models.Model):
#     admin = models.OneToOneField(Customeruser, on_delete=models.CASCADE)
#     address = models.TextField()
#     gender = models.CharField(max_length=100)
#     room_number = models.CharField(max_length=100)
#     phone_number = models.IntegerField(max_length=12)
#     roll_number = models.IntegerField(max_length=10)





class Student(models.Model):
    user = models.OneToOneField(Customeruser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    # hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    # balance = models.DecimalField(max_digits=6, decimal_places=2)
    course_id = models.ForeignKey(course, default='1',null=True,blank=True,  on_delete= models.DO_NOTHING)
    session_year_id = models.ForeignKey(Session_Year,default='SESSION_ YEAR',null=True,blank=True,  on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

# class Hostel(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name

class Staff(models.Model):
    admin =models.OneToOneField(Customeruser,on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=50)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.admin.username
    

class Staff_Notification(models.Model):
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.staff_id.admin.first_name
    

class Staff_leave(models.Model):
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    to_date = models.CharField(max_length=100,default=0)
    days = models.IntegerField(default=0)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_id.admin.first_name + self.staff_id.admin.last_name
    


class Staff_Feedback(models.Model):
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField(null=True)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.staff_id.admin.first_name + " " + self.staff_id.admin.last_name


class Student_Notification(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.student_id.user.first_name
    

class Student_Feedback(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField(null=True)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.student_id.user.first_name + " " + self.student_id.user.last_name





# class Mess_off_leave(models.Model):
#     student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
#     off_date = models.CharField(max_length=100)
#     on_date = models.CharField(max_length=100)
#     message = models.TextField()
#     status = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     #days=models.IntegerField(default=0)

#     def __str__(self):
#         return self.student_id.user.first_name + self.student_id.user.last_name



class Mess_off_leave(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    off_date = models.DateField()
    on_date = models.DateField()
    days = models.IntegerField(default=0)
    message = models.TextField()

    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_id.user.first_name + ' : ' + str(self.off_date) + ' - ' + str(self.on_date)
    
    # @property
    # def days(self):
    #     return (self.on_date - self.off_date).days + 1






class Attendance(models.Model):

    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.attendance_date)


class Attendance_Report(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.DO_NOTHING)    
    attendance_id = models.ForeignKey(Attendance,on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return   f"{self.student_id.roll_number} - {self.student_id.user.get_full_name()} ({self.attendance_id.attendance_date}): {'Present' if self.present else 'Absent'}"

#mess

class Mess(models.Model):
    day = models.CharField(max_length=10)
    breakfast=models.TextField(max_length=100)
    lunch=models.TextField(max_length=100)
    dinner=models.TextField(max_length=100)
    def _str_(self):
         return self.day
    

    
class Billing(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=10)
    year = models.IntegerField()
    days_of_leave_taken = models.PositiveIntegerField(default=0)  # Change field type to integer
    total_days_in_month = models.IntegerField()
    amount_due = models.DecimalField(max_digits=6, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    def __str__(self):
         return self.student.user.first_name + self.month
