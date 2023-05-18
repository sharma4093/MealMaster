from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Staff,Staff_Notification,Staff_leave,Staff_Feedback,Student,Attendance,Attendance_Report,Billing,Mess_off_leave
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from calendar import monthrange
from django.utils import timezone
# import datetime
from decimal import Decimal
import calendar


@login_required(login_url='/')
def HOME(request):
    return render(request ,'staff/staff_home.html')


@login_required(login_url='/')
def NOTIFICATIONS(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id
        notification = Staff_Notification.objects.filter(staff_id = staff_id)

        context = { 
            'notification': notification,
        }
    return render(request,'staff/notification.html',context)


@login_required(login_url='/')
def STAFF_NOTIFICATION_MARK_DONE(request,status):
    notification = Staff_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('notifications')



@login_required(login_url='/')
def STAFF_APPLY_LEAVE(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_leave.objects.filter(staff_id = staff_id)
        context = {
             'staff_leave_history':staff_leave_history,
        }
    return render(request,'staff/apply_leave.html',context)




@login_required(login_url='/')
# def STAFF_APPLY_LEAVE_SAVE(request):
#     if request.method == "POST":

#         leave_date = request.POST.get('leave_date')
#         leave_message = request.POST.get('leave_message')
#         staff = Staff.objects.get(admin = request.user.id)
#         leave = Staff_leave(
#             staff_id = staff,
#             date = leave_date,
#             message = leave_message,
#         )
#         leave.save()
#         messages.success(request,'leave applied successfully')
#         return redirect('staff_apply_leave')
    

def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        to_date = request.POST.get('to_date')
        leave_message = request.POST.get('leave_message')
        staff = Staff.objects.get(admin=request.user.id)
        today = timezone.now().date()

        try:
            leave_date = datetime.datetime.strptime(leave_date, "%Y-%m-%d").date()
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD format.")
            return redirect('staff_apply_leave')

        if leave_date <= today:
            messages.error(request, "Leave cannot be applied for past or presenet dates.")
            return redirect('staff_apply_leave')
        
        if leave_date >= to_date:
            messages.error(request, "Start date must be before end date.")
            return redirect('staff_apply_leave')
        
        # check if staff has already applied for leave during the requested dates
        leaves = Staff_leave.objects.filter(staff_id=staff)
        for leave in leaves:
            leave_from_date = datetime.datetime.strptime(str(leave.date), '%Y-%m-%d').date()
            leave_to_date = datetime.datetime.strptime(str(leave.to_date), '%Y-%m-%d').date()

            if leave_date <= leave_to_date and to_date >= leave_from_date:

            # if leave_date <= leave.to_date and to_date >= leave.date:
                messages.error(request, "Leave already applied for overlapping dates.")
                return redirect('staff_apply_leave')

        days = (to_date - leave_date).days + 1

        leave = Staff_leave(
            staff_id=staff,
            date=leave_date,
            to_date=to_date,
            message=leave_message,
            days=days,
        )
        leave.save()
        messages.success(request,'Leave applied successfully')
        return redirect('staff_apply_leave')




def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin = request.user.id)

    feedback_history = Staff_Feedback.objects.filter(staff_id = staff_id)

    context = {
        'feedback_history':feedback_history,
    }
    return render(request,'staff/feedback.html',context)



def STAFF_FEEDBACK_SAVE(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')

        staff = Staff.objects.get(admin = request.user.id)
        feedback = Staff_Feedback(
            staff_id =  staff,
            feedback = feedback,
            feedback_reply = "",
        )
        feedback.save()
        messages.success(request,'feedback sent successfully')
        return redirect('staff_feedback')
    

@login_required(login_url='/login/')
def STAFF_TAKE_ATTENDANCE(request):
    date = datetime.now().date()
    attendance = Attendance.objects.filter(attendance_date=date).first()
    if not attendance:
        attendance = Attendance.objects.create(
            attendance_date=date
        )
    students = Student.objects.all()
    if request.method == 'POST':
        for student in students:
            present = False
            if str(student.id) in request.POST:
                present = True
            Attendance_Report.objects.create(
                student_id=student,
                attendance_id=attendance,
                present=present,
            )
            #messages.success(request,'marked attendance successfully')
        return redirect('attendance_report')
    return render(request, 'staff/take_attendance.html', {'students': students, 'date': date})



@login_required(login_url='/login/')
def attendance_report(request):
    date = datetime.now().date()
    attendance = Attendance.objects.filter(attendance_date=date).first()
    if not attendance:
        return render(request, 'staff/attendance_report.html')
    reports = Attendance_Report.objects.filter(attendance_id=attendance)
    report_data = []
    for report in reports:
        student = report.student_id
        status = "Absent"
        if report.present:
            status = "Present"
        report_data.append({
            'name': student.user.first_name + ' ' + student.user.last_name,
            'roll_number': student.roll_number,
            'status': status,
            'date': date,
        })
    return render(request, 'staff/attendance_report.html', {'report_data': report_data})



# def generate_bill(request):
#     if request.method == 'POST':
#         # Retrieve form data
#         student_id = request.POST['student_id']
#         month = int(request.POST['month'])
#         year = int(request.POST['year'])

#         # Retrieve mess off leave records for the selected student and month
#         mess_off_leaves = Mess_off_leave.objects.filter(student_id=student_id, off_date__month=month, off_date__year=year)

#         # Calculate the number of billable days in the selected month
#         total_days_in_month = monthrange(year, month)[1]
#         days_on_leave = 0
#         for mess_off_leave in mess_off_leaves:
#             days_on_leave += (mess_off_leave.on_date - mess_off_leave.off_date).days + 1
#         billable_days = total_days_in_month - days_on_leave

#         # Calculate the bill amount based on the number of billable days and fixed meal cost
#         meal_cost = 105  # Change this to the actual cost per meal
#         amount_due = billable_days * meal_cost

#         # Save the bill to the database
#         student = Student.objects.get(pk=student_id)
#         billing = Billing(student=student, month=month, year=year, days_of_leave_taken=days_on_leave,
#                           total_days_in_month=total_days_in_month, amount_due=amount_due)
#         billing.save()

#         messages.success(request, 'Bill generated successfully')
#         return redirect('generate_bill')

#     students = Student.objects.all()
#     context = {'students': students}
#     return render(request, 'staff/generate_bill.html', context)


# def generate_bill(request):
#     if request.method == 'POST':
#         month = int(request.POST.get('month'))
#         year = int(request.POST.get('year'))
#         cost_per_day = float(request.POST.get('cost_per_day'))

#         # Retrieve all students
#         students = Student.objects.all()

#         # Calculate bill for each student
#         for student in students:
#             # Retrieve mess off leave records for the given month and year
#             mess_off_leaves = Mess_off_leave.objects.filter(student_id=student.id, off_date__month=month, off_date__year=year)

#             # Calculate total days of leave taken by the student
#             total_days_of_leave_taken = sum([leave.days for leave in mess_off_leaves])

#             # Calculate total days in the month
#             total_days_in_month = monthrange(year, month)[1]

#             # Calculate amount due
#             amount_due = Decimal(total_days_in_month - total_days_of_leave_taken) * Decimal(cost_per_day)

#             # Save the billing record for the student
#             billing = Billing(student=student, month=month, year=year, days_of_leave_taken=total_days_of_leave_taken,
#                               total_days_in_month=total_days_in_month, amount_due=amount_due)
#             billing.save()

#         return render(request, 'staff/generate_bill.html', {'month': datetime.strptime(str(month), '%m').strftime('%B'), 'year': year})

#     return render(request, 'staff/generate_bill.html')



# def generate_bill(request):
#     if request.method == 'POST':
#         month = int(request.POST.get('month'))
#         year = int(request.POST.get('year'))
#         cost_per_day = float(request.POST.get('cost_per_day'))

#         # Check if bill has already been generated for this month and year
#         if Billing.objects.filter(month=month, year=year).exists():
#             return render(request, 'staff/generate_bill.html', {'message': f'Bill for {datetime.strptime(str(month), "%m").strftime("%B")} {year} has already been generated.'})

#         # Retrieve all students
#         students = Student.objects.all()

#         # List to store generated bills
#         bills = []

#         # Calculate bill for each student
#         for student in students:
#             # Retrieve mess off leave records for the given month and year
#             mess_off_leaves = Mess_off_leave.objects.filter(student_id=student.id, off_date__month=month, off_date__year=year)

#             # Calculate total days of leave taken by the student
#             total_days_of_leave_taken = sum([leave.days for leave in mess_off_leaves])

#             # Calculate total days in the month
#             total_days_in_month = monthrange(year, month)[1]

#             # Calculate amount due
#             amount_due = Decimal(total_days_in_month - total_days_of_leave_taken) * Decimal(cost_per_day)

#             # Save the billing record for the student
#             billing = Billing(student=student, month=month, year=year, days_of_leave_taken=total_days_of_leave_taken,
#                               total_days_in_month=total_days_in_month, amount_due=amount_due)
#             billing.save()

#             # Add billing record to list of generated bills
#             bills.append(billing)

#         return render(request, 'staff/generate_bill.html', {'month': datetime.strptime(str(month), '%m').strftime('%B'), 'year': year, 'bills': bills})

#     return render(request, 'staff/generate_bill.html')


# def generate_bill(request):
#     if request.method == 'POST':
#         month = int(request.POST.get('month'))
#         year = int(request.POST.get('year'))
#         cost_per_day = float(request.POST.get('cost_per_day'))

#         # Retrieve all students
#         students = Student.objects.all()

#         # Calculate bill for each student
#         for student in students:
#             # Retrieve mess off leave records for the given month and year
#             mess_off_leaves = Mess_off_leave.objects.filter(student_id=student.id, off_date__month=month, off_date__year=year, status=1)

#             # Calculate total days of leave taken by the student
#             total_days_of_leave_taken = sum([leave.days for leave in mess_off_leaves])

#             # Calculate total days in the month
#             total_days_in_month = monthrange(year, month)[1]

#             # Calculate amount due
#             amount_due = Decimal(total_days_in_month - total_days_of_leave_taken) * Decimal(cost_per_day)

#             # Save the billing record for the student
#             billing = Billing(student=student, month=month, year=year, days_of_leave_taken=total_days_of_leave_taken,
#                               total_days_in_month=total_days_in_month, amount_due=amount_due)
#             billing.save()

#         # Check if billing records were generated for the given month and year
#         bill_generated = Billing.objects.filter(month=month, year=year).exists()

#         if bill_generated:
#             message = f"Billing records for {datetime.strptime(str(month), '%m').strftime('%B')}, {year} have already been generated."
#         else:
#             message = f"Billing records for {datetime.strptime(str(month), '%m').strftime('%B')}, {year} have been generated successfully."

#         # Retrieve all billing records for the given month and year
#         billing_records = Billing.objects.filter(month=month, year=year)

#         return render(request, 'staff/view_list_bill.html', {'message': message, 'billing_records': billing_records})

#     return render(request, 'staff/generate_bill.html')


def generate_bill(request):
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        cost_per_day = float(request.POST.get('cost_per_day'))

        # Check if billing records already exist for the given month and year
        if Billing.objects.filter(month=month, year=year).exists():
            message = f"Billing records for {datetime.strptime(str(month), '%m').strftime('%B')}, {year} have already been generated."
            billing_records = Billing.objects.filter(month=month, year=year)
        else:
            # Retrieve all students
            students = Student.objects.all()

            # Calculate bill for each student
            for student in students:
                # Retrieve mess off leave records for the given month and year
                mess_off_leaves = Mess_off_leave.objects.filter(student_id=student.id, off_date__month=month, off_date__year=year, status=1)

                # Calculate total days of leave taken by the student
                total_days_of_leave_taken = sum([leave.days for leave in mess_off_leaves])

                # Calculate total days in the month
                total_days_in_month = monthrange(year, month)[1]

                # Calculate amount due
                amount_due = Decimal(total_days_in_month - total_days_of_leave_taken) * Decimal(cost_per_day)

                # Save the billing record for the student
                billing = Billing(student=student, month=month, year=year, days_of_leave_taken=total_days_of_leave_taken,
                                  total_days_in_month=total_days_in_month, amount_due=amount_due)
                billing.save()

            message = f"Billing records for {datetime.strptime(str(month), '%m').strftime('%B')}, {year} have been generated successfully."

            # Retrieve all billing records for the given month and year
            billing_records = Billing.objects.filter(month=month, year=year)

        return render(request, 'staff/view_list_bill.html', {'message': message, 'billing_records': billing_records})

    return render(request, 'staff/generate_bill.html')