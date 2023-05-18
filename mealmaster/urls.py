"""mealmaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .import views,owner_views,staff_views,student_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE,name='base'),
    # login path
    path('', views.MAIN,name='home'),
    path('home/login', views.LOGIN,name='login'),
    path('home/login/student', views.LOGIN1,name='login_student'),
    path('home/login/staff', views.LOGIN2,name='login_staff'),
    path('doLogin', views.doLogin,name='dologin'),
    path('doLogout', views.doLogout,name='logout'),

    #profile update

    path('profile', views.PROFILE,name='profile'),
    path('profile/update', views.PROFILE_UPDATE,name='profile_update'),



    #owner panel url or hod
    path('OWNER/Home', owner_views.Home,name='owner_home'),
    path('OWNER/student/add', owner_views.ADD_STUDENT,name='add_student'),
    path('OWNER/student/View', owner_views.VIEW_STUDENT,name='view_student'),
    path('OWNER/student/details/<str:id>',owner_views.STUDENT_DETAILS, name='student_details'),
    path('OWNER/student/Edit/<str:id>', owner_views.EDIT_STUDENT,name='edit_student'),
    path('OWNER/student/Update', owner_views.UPDATE_STUDENT,name='update_student'),
    path('OWNER/student/Delete/<str:user>', owner_views.DELETE_STUDENT,name='delete_student'),
    path('OWNER/staff/details/<str:id>', owner_views.STAFF_DETAILS ,name='staff_details'),





    # staff add and view
    path('OWNER/Staff/add', owner_views.ADD_STAFF,name='add_staff'),
    path('OWNER/Staff/view', owner_views.VIEW_STAFF,name='view_staff'),
    path('OWNER/Staff/Edit/<str:id>', owner_views.EDIT_STAFF,name='edit_staff'),
    path('OWNER/Staff/Update', owner_views.UPDATE_STAFF,name='update_staff'),
    path('OWNER/Staff/Delete/<str:admin>', owner_views.DELETE_STAFF,name='delete_staff'),

    path('OWNER/Staff/Send_Notification', owner_views.STAFF_SEND_NOTIFICATION,name='staff_send_notification'),
    path('OWNER/Staff/save_notification', owner_views.SAVE_STAFF_NOTIFICATION,name='save_staff_notification'),

    path('OWNER/staff/leave_view',owner_views.STAFF_LEAVE_VIEW,name='staff_leave_view'),
    path('OWNER/staff/approve_leave/<str:id>',owner_views.STAFF_APPROVE_LEAVE,name='staff_approve_leave'),
    path('OWNER/staff/disapprove_leave/<str:id>',owner_views.STAFF_DISAPPROVE_LEAVE,name='staff_disapprove_leave'),
    path('OWNER/Staff/feedback', owner_views.STAFF_FEEDBACK,name='staff_feedback_reply'),
    path('OWNER/Staff/feedback/save', owner_views.STAFF_FEEDBACK_SAVE,name='staff_feedback_reply_save'),

    path('OWNER/student/mess_off_view',owner_views.STUDENT_MESS_OFF_VIEW,name='student_mess_off_view'),
    path('OWNER/student/approve_mess_off_leave/<str:id>',owner_views.STUDENT_MESS_OFF_APPROVE_LEAVE,name='student_mess_off_approve_leave'),
    path('OWNER/student/disapprove_leave/<str:id>',owner_views.STUDENT_MESS_OFF_DISAPPROVE_LEAVE,name='student_mess_off_disapprove_leave'),


    path('OWNER/Student/feedback', owner_views.STUDENT_FEEDBACK,name='student_feedback_reply'),
    path('OWNER/Student/feedback/reply/save', owner_views.REPLY_STUDENT_FEEDBACK,name='reply_student_feedback'),

    path('OWNER/student/Send_Notification', owner_views.STUDENT_SEND_NOTIFICATION,name='student_send_notification'),
    path('OWNER/Student/save_notification', owner_views.SAVE_STUDENT_NOTIFICATION,name='save_student_notification'),

    path('OWNER/view_bills',owner_views.view_list_bill,name='view_bill'),

        # coursesor menu


      # all urls of staff panel now here and its views in staff views file
    path('staff/Home', staff_views.HOME,name='staff_home'),
    path('staff/Notifications',staff_views.NOTIFICATIONS,name='notifications'),
    path('staff/mark_as_done/<status>',staff_views.STAFF_NOTIFICATION_MARK_DONE,name='staff_notification_mark_done'),

    path('staff/Apply_leave',staff_views.STAFF_APPLY_LEAVE,name='staff_apply_leave'),
    path('staff/Apply_leave_save',staff_views.STAFF_APPLY_LEAVE_SAVE,name='staff_apply_leave_save'),
    path('staff/Feedback',staff_views.STAFF_FEEDBACK,name='staff_feedback'),
    path('staff/Feedback/save',staff_views.STAFF_FEEDBACK_SAVE,name='staff_feedback_save'),
 
    path('staff/Take_Attendance',staff_views.STAFF_TAKE_ATTENDANCE,name='staff_take_attendance'),

    path('staff/view_Attendance',staff_views.attendance_report,name='attendance_report'),




    # student panel urls 
    path('student/Home', student_views.Home,name='student_home'),
    path('student/Notifications',student_views.STUDENT_NOTIFICATION,name='student_notification'),
    path('student/mark_as_done/<status>',student_views.STUDENT_NOTIFICATION_MARK_DONE,name='student_notification_mark_done'),
    path('student/Feedback',student_views.STUDENT_FEEDBACK,name='student_feedback'),
    path('student/Feedback/save',student_views.STUDENT_FEEDBACK_SAVE,name='student_feedback_save'),

    path('student/Mess_off',student_views.STUDENT_MESS_OFF,name='student_mess_off'),
    path('student/Mess_leave_save',student_views.STUDENT_MESS_LEAVE_SAVE,name='student_mess_leave_save'),

#menu

    path('OWNER/mess-menu/view', owner_views.VIEW_MENU, name='view_menu'),
    path('OWNER/mess-menu/add', owner_views.ADD_MENU, name='add_menu'),
    path('OWNER/mess-menu/edit-menu', owner_views.EDIT_MENU, name='edit_menu'),
    path('OWNER/edit_menu/Update/<str:id>', owner_views.UPDATE_MENU,name='update_menu'),
    path('OWNER/mess-menu/save_update', owner_views.SAVE_UPDATE_MENU, name='save_update_menu'),
    path('OWNER/mess-menu/Delete/<str:id>', owner_views.DELETE_MENU,name='delete_menu'),


# generate bill urls
    path('staff/generate_bill/', staff_views.generate_bill, name='generate_bill'),
    path('student/view_bills/', student_views.view_bills, name='view_bills'),
    
    # path('student/view_bills/<str:student_id>/', student_views.view_bills, name='view_bills'),
    
    #path('pay-bill/<int:bill_id>/', student_views.pay_bill, name='pay_bill'),









]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


