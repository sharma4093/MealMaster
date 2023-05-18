from django.contrib import admin
from .models import*
from django.contrib.auth.admin import UserAdmin

from app.models import Customeruser,course,Session_Year,Student,Staff,Staff_Notification,Mess

# Register your models here.

class UserModel(admin.ModelAdmin):
    list_display=['username','user_type']



admin.site.register(Customeruser,UserModel)

admin.site.register(course)
admin.site.register(Session_Year)
admin.site.register(Student)
# admin.site.register(Hostel)
admin.site.register(Staff)

admin.site.register(Staff_Notification)
admin.site.register(Staff_leave)

admin.site.register(Staff_Feedback)
admin.site.register(Student_Notification)

admin.site.register(Student_Feedback)
admin.site.register(Mess_off_leave)

admin.site.register(Attendance)
admin.site.register(Attendance_Report)

admin.site.register(Mess)


admin.site.register(Billing)

