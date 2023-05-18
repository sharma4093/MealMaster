import datetime
from django.shortcuts import render,redirect
from app.models import Student_Notification,Student,Student_Feedback,Mess_off_leave,Billing
from django.contrib import messages

from django.utils import timezone
from django.http import HttpResponseBadRequest


def Home(request):
    return render(request,'student/home.html')

def STUDENT_NOTIFICATION(request):
    student = Student.objects.filter(user = request.user.id)
    for i in student:
        #print(student)
        student_id = i.id
        notification = Student_Notification.objects.filter(student_id = student_id)
        context = {
            'notification':notification,
        }
    return render(request,'student/notification.html',context)

def STUDENT_NOTIFICATION_MARK_DONE(request,status):
    notification = Student_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()

    return redirect('student_notification')

def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(user = request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id = student_id)

    context ={
        'feedback_history':feedback_history,
        
    }
    return render(request,'student/feedback.html',context)


def STUDENT_FEEDBACK_SAVE(request):

    if request.method == "POST":
        feedback = request.POST.get('feedback')

        student = Student.objects.get(user = request.user.id)
        feedbacks = Student_Feedback(
            student_id = student,
            feedback = feedback,
            feedback_reply ="",
        )
        feedbacks.save()
        return redirect('student_feedback')



def STUDENT_MESS_OFF(request):
    student = Student.objects.get(user = request.user.id)
    mess_off_history = Mess_off_leave.objects.filter(student_id = student)
    
    context = {
        'mess_off_history':mess_off_history,
    }

    return render(request,'student/mess_off.html',context)



# def STUDENT_MESS_LEAVE_SAVE(request):
#     if request.method =="POST":
#         off_date = request.POST.get('off_date')
#         on_date = request.POST.get('on_date')
#         leave_message = request.POST.get('leave_message')
#        # days = abs(on_date-off_date)-1

#         student_id = Student.objects.get(user = request.user.id)
#         mess_off_leave = Mess_off_leave(
#             student_id = student_id,
#             off_date = off_date,
#             on_date = on_date,
#             message = leave_message,
#             #days=days
            
#         )
#         mess_off_leave.save()
#         messages.success(request,'mess off leave applied successfully')
#         return redirect('student_mess_off')


# def STUDENT_MESS_LEAVE_SAVE(request):
#     if request.method == "POST":
#         off_date_str = request.POST.get('off_date')
#         on_date_str = request.POST.get('on_date')
#         leave_message = request.POST.get('leave_message')

#         # Parse the off_date and on_date strings into datetime objects
#         off_date = timezone.make_aware(datetime.datetime.strptime(off_date_str, '%Y-%m-%d'))
#         on_date = timezone.make_aware(datetime.datetime.strptime(on_date_str, '%Y-%m-%d'))

#         # Check that the leave period is at least one day
        
#         if (on_date - off_date).days < 1:
#             return HttpResponseBadRequest('The leave period must be at least one day.')

#         # Check that the leave period starts from today or a future date
#         today = datetime.datetime.now().date()
#         off_date = datetime.datetime.strptime(request.POST.get('off_date'), "%Y-%m-%d").date()
#         if off_date < today:
#             return HttpResponseBadRequest('The leave period cannot start from a past date.')

#         student_id = Student.objects.get(user=request.user.id)
#         mess_off_leave = Mess_off_leave(
#             student_id=student_id,
#             off_date=off_date,
#             on_date=on_date,
#             message=leave_message,
#         )
#         mess_off_leave.save()
#         messages.success(request, 'Mess off leave applied successfully')
#         return redirect('student_mess_off')





def STUDENT_MESS_LEAVE_SAVE(request):
    if request.method == "POST":
        off_date = request.POST.get('off_date')
        on_date = request.POST.get('on_date')
        leave_message = request.POST.get('leave_message')

        student_id = Student.objects.get(user=request.user.id)
        today = timezone.now().date()

        try:
            off_date = datetime.datetime.strptime(off_date, "%Y-%m-%d").date()
            on_date = datetime.datetime.strptime(on_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD format.")
            return redirect('student_mess_off')

        if off_date <= today:
            messages.error(request, "Leave cannot be applied for past or present dates.")
            return redirect('student_mess_off')

        if off_date >= on_date:
            messages.error(request, "Start date must be before end date.")
            return redirect('student_mess_off')
        
        
        # Check if student has already applied for leave during requested dates
        leaves = Mess_off_leave.objects.filter(student_id=student_id)
        for leave in leaves:
            if off_date <= leave.on_date and on_date >= leave.off_date:
                messages.error(request, "Leave already applied for overlapping dates.")
                return redirect('student_mess_off')

        days = (on_date - off_date).days + 1

        mess_off_leave = Mess_off_leave(
            student_id=student_id,
            off_date=off_date,
            on_date=on_date,
            message=leave_message,
            days=days
        )
        mess_off_leave.save()
        messages.success(request, 'Mess off leave applied successfully.')
        return redirect('student_mess_off')








# def view_bills(request):
#    student = request.user.student
#    bills = Billing.objects.filter(student=student)
#    context = {'student': student, 'bills': bills}
#    return render(request, 'student/view_bills.html', context)



def view_bills(request):
    student = Student.objects.get(user=request.user)
    bills = Billing.objects.filter(student=student)
    return render(request, 'student/view_bills.html', {'bills': bills})