from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import course,Session_Year,Customeruser,Student,Staff, Staff_Notification,Staff_leave,Staff_Feedback,Student_Notification,Student_Feedback,Mess_off_leave,Mess,Billing
from django.contrib import messages
#DECORATOR FOR AVOIDING DIRECT ACCESS TO OWNER PANEL USING URL


@login_required(login_url='/')
def Home(request):
    student_Count = Student.objects.all().count()
    staff_Count = Staff.objects.all().count()

    student_gender_male = Student.objects.filter(gender = 'Male').count()
    student_gender_female = Student.objects.filter(gender = 'Female').count()

    context ={
         'student_Count':student_Count,
         'staff_Count':staff_Count,
         'student_gender_male':student_gender_male,
         'student_gender_female':student_gender_female,

    }
    return render(request, 'owner/home.html',context)

@login_required(login_url='/')
def ADD_STUDENT(request):
    Course = course.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == "POST":
        Profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        Roll_num = request.POST.get('Roll_num')
        Room_Number = request.POST.get('Room_Number')
        Mobile_Number = request.POST.get('Mobile_Number')
        address = request.POST.get('address')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        # print(Profile_pic,first_name,last_name,email,username,password,gender,course_id,Roll_num,session_year_id,Room_Number,Mobile_Number,address)

        if Customeruser.objects.filter(email=email).exists():
            messages.warning(request,'Email already registered')
            return redirect('add_student')
        if Customeruser.objects.filter(username=username).exists():
            messages.warning(request,'usernaame already registered')
            return redirect('add_student')
        else:
            user = Customeruser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = Profile_pic,
                user_type = 3

            )
            user.set_password(password)
            user.save()

            Course = course.objects.get(id = course_id)
            # session_year = Session_Year.objects.get(id = session_year_id)
            session_year = Session_Year.objects.get(id = session_year_id) 
            student = Student.objects.create(
                user = user,
                address =address,
                session_year_id = session_year,
                course_id = Course,
                gender = gender,
                roll_number = Roll_num,
                room_number = Room_Number,
                phone_number = Mobile_Number,

            )
            student.save()
            messages.success(request, user.first_name + " "+ user.last_name + " "+' saved successfully')
            return redirect('add_student')

    context = {
        'Course': Course,
        'session_year' : session_year,
    }
    return render(request, 'owner/add_student.html',context)


@login_required(login_url='/')
def VIEW_STUDENT(request):
    student =Student.objects.all()
    context = { 
        'student': student,
    }
    return render(request,'owner/view_student.html',context)

@login_required(login_url='/')

def STUDENT_DETAILS(request, id):
     student_detail = Student.objects.filter(id=id)
     context = {'student': student_detail}
     return render(request, 'owner/student_details.html', context)

 


@login_required(login_url='/')
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id = id)
    Course = course.objects.all()
    session_year=Session_Year.objects.all()
    context = { 
        'student': student,
        'Course': Course,
        'session_year' : session_year,
    }
    return render(request,'owner/edit_student.html',context)


@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        # present in user model
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # present in student model
        gender = request.POST.get('gender')
        Roll_num = request.POST.get('Roll_num')
        Room_Number = request.POST.get('Room_Number')
        Mobile_Number = request.POST.get('Mobile_Number')
        address = request.POST.get('address')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        # update in user model using id - if got id  then save user data

        user = Customeruser.objects.get(id=student_id)
        user.profile_pic =profile_pic
        user.first_name =first_name
        user.last_name =last_name
        user.email=email
        user.username =username

        if password != None and password != "":
                user.set_password(password)

        if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic
        user.save()

        # update in student model using id
        student = Student.objects.get(user =student_id)
        student.address=address
        student.gender =gender
        student.roll_number=Roll_num
        student.room_number=Room_Number
        student.phone_number=Mobile_Number

        # using course model for id -courseid=id
        Course = course.objects.get(id = course_id)
        student.course_id = Course
        #  using session year model to have id to update
        session_year = Session_Year.objects.get(id =session_year_id)
        student.session_year_id=session_year

        student.save()
        messages.success(request,'records are successfully updated')
        return redirect('view_student')

    return render(request,'owner/edit_student.html')


@login_required(login_url='/')
def DELETE_STUDENT(request,user):
     student =Customeruser.object.get(id = user)
     student.delete()
     messages.success(request,'records are successfully deleted!!')
     return redirect('view_student')



# courses CRUD FOR Menu not 
@login_required(login_url='/')
def ADD_STAFF(request):
     if request.method =="POST":
          profile_pic=request.FILES.get('profile_pic')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          email = request.POST.get('email')
          username = request.POST.get('username')
          password = request.POST.get('password')
          address = request.POST.get('address')
          gender = request.POST.get('gender')

        #   print(profile_pic,first_name,last_name,email,username,password,address,gender)


          if Customeruser.objects.filter(email=email).exists():
            messages.warning(request,'Email already registered')
            return redirect('add_staff')
          if Customeruser.objects.filter(username=username).exists():
            messages.warning(request,'username already registered')
            return redirect('add_staff')
          else:
              user =Customeruser(first_name=first_name,last_name=last_name,email=email,username=username,profile_pic=profile_pic,user_type = 2)
              user.set_password(password)
              user.save()

              staff=Staff(
                  admin=user,
                  address=address,
                  gender=gender
              )
              staff.save()
              messages.success(request,'staff is auccessfully added')
              return redirect('add_staff')
     return render(request,'owner/add_staff.html')


@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {'staff':staff,}
    return render(request,'owner/view_staff.html',context)




@login_required(login_url='/')
def STAFF_DETAILS(request, id):
    staff_detail = Staff.objects.filter(id=id)
    context = {'staff': staff_detail}
    return render(request, 'owner/staff_details.html', context)


@login_required(login_url='/')
def EDIT_STAFF(request,id):
    staff = Staff.objects.get(id = id)
    context ={'staff':staff}
    return render(request,'owner/edit_staff.html',context)


@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method =="POST":
          staff_id = request.POST.get('staff_id') 
          profile_pic=request.FILES.get('profile_pic')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          email = request.POST.get('email')
          username = request.POST.get('username')
          password = request.POST.get('password')
          address = request.POST.get('address')
          gender = request.POST.get('gender')
   #   in customuser model
          user=Customeruser.objects.get(id=staff_id)
          user.username = username
          user.first_name = first_name
          user.last_name = last_name
          user.email = email

          if password != None and password != "":
               user.set_password(password)

          if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic

          user.save()      
  #   in staff model
          staff = Staff.objects.get(admin = staff_id)
          staff.gender = gender
          staff.address = address

          staff.save()
          messages.success(request,'staff is successfully updated')
          return redirect('view_staff')

    return render(request,'owner/edit_staff.html')


@login_required(login_url='/')
def DELETE_STAFF(request, admin):
     staff= Customeruser.objects.get(id = admin)
     staff.delete()
     messages.success(request,'record successfully deleted')
     return redirect('view_staff')


@login_required(login_url='/')
def STAFF_SEND_NOTIFICATION(request):
     staff = Staff.objects.all()
     see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]  
#see notification in order and only recent last 5 notifications
     context = {
          'staff':staff,
          'see_notification':see_notification,
     }
     return render(request,'owner/staff_notification.html',context)


@login_required(login_url='/')
def SAVE_STAFF_NOTIFICATION(request):
     if request.method == "POST":
          staff_id = request.POST.get('staff_id')
          message = request.POST.get('message')
          staff = Staff.objects.get( admin=staff_id )
          notification = Staff_Notification(
               staff_id = staff,
               message= message,
          )
          notification.save()
          messages.success(request,'notification sent')
     return redirect('staff_send_notification')


@login_required(login_url='/')
def STAFF_LEAVE_VIEW(request):
     staff_leave = Staff_leave.objects.all()
     context = {
          'staff_leave': staff_leave,
     }
     return render(request,'owner/staff_leave.html',context)


@login_required(login_url='/')
def STAFF_APPROVE_LEAVE(request,id):
     leave = Staff_leave.objects.get(id = id)
     leave.status = 1
     leave.save()
     return redirect('staff_leave_view')


@login_required(login_url='/')
def STAFF_DISAPPROVE_LEAVE(request,id):
     leave = Staff_leave.objects.get(id = id)
     leave.status = 2
     leave.save()
     return redirect('staff_leave_view')



def STUDENT_MESS_OFF_VIEW(request):
     mess_off_leave = Mess_off_leave.objects.all()

     context ={
          'mess_off_leave':mess_off_leave,

     }
     return render(request,'owner/student_mess_off.html',context)

@login_required(login_url='/')
def STUDENT_MESS_OFF_APPROVE_LEAVE(request,id):
     leave = Mess_off_leave.objects.get(id = id)
     leave.status = 1
     leave.save()
     return redirect('student_mess_off_view')


@login_required(login_url='/')
def STUDENT_MESS_OFF_DISAPPROVE_LEAVE(request,id):
     leave = Mess_off_leave.objects.get(id = id)
     leave.status = 2
     leave.save()
     return redirect('student_mess_off_view')








def STAFF_FEEDBACK(request):
     feedback = Staff_Feedback.objects.all()
     feedback_history = Staff_Feedback.objects.all().order_by('-id')[0:5]

     context = {
          'feedback':feedback,
          'feedback_history':feedback_history,
     }
     return render(request,'owner/staff_feedback.html',context)


def STAFF_FEEDBACK_SAVE(request):
     if request.method == "POST":
          feedback_id = request.POST.get('feedback_id')
          feedback_reply = request.POST.get('feedback_reply')

          feedback = Staff_Feedback.objects.get(id = feedback_id)
          feedback.feedback_reply = feedback_reply
          feedback.status = 1
          feedback.save()
          messages.success(request,'feedback replied successfully')
          return redirect('staff_feedback_reply')
     

def STUDENT_FEEDBACK(request):
     feedback = Student_Feedback.objects.all()
     feedback_history = Student_Feedback.objects.all().order_by('-id')[0:5]

     context = {
          'feedback':feedback,
          'feedback_history':feedback_history,
     }
     return render(request,'owner/student_feedback.html',context)


def REPLY_STUDENT_FEEDBACK(request):
     if request.method == "POST":
          feedback_id = request.POST.get('feedback_id')
          feedback_reply = request.POST.get('feedback_reply')
          
          feedback = Student_Feedback.objects.get(id = feedback_id)
          feedback.feedback_reply = feedback_reply
          feedback.status = 1
          feedback.save()
          messages.success(request,'feedback replied successfully')
          return redirect('student_feedback_reply')

def STUDENT_SEND_NOTIFICATION(request):
          student = Student.objects.all()
          notification = Student_Notification.objects.all()
         
          context ={
               'student':student,
               'notification':notification,
          }
          return render(request,'owner/student_notification.html',context)

def SAVE_STUDENT_NOTIFICATION(request):
     if request.method == "POST":
          message = request.POST.get('message')
          student_id = request.POST.get('student_id')

          student = Student.objects.get(user = student_id)
         
          stud_notification = Student_Notification(
          student_id = student,
          message = message,
          )
          stud_notification.save()
          messages.success(request,'sent successfully')
          return redirect('student_send_notification')





def VIEW_MENU(request):

    Menu = Mess.objects.all()
    context = {
        'day': Menu,
    }
    return render(request, 'owner/view_menu.html', context)


def ADD_MENU(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        breakfast = request.POST.get('breakfast')
        lunch = request.POST.get('lunch')
        dinner = request.POST.get('dinner')
        mess = Mess(day=day, breakfast=breakfast, lunch=lunch, dinner=dinner)
        mess.save()
        messages.success(request, 'Menu is successfully added')
    # got error of else: removed and fixed
    return render(request, 'owner/add_menu.html')

# edit menu table


def EDIT_MENU(request):
    # Menu = Mess.objects.get(id=id)
    Menu = Mess.objects.all()
    context = {
        'day': Menu,
    }
    return render(request, 'owner/edit_menu.html', context)

def UPDATE_MENU(request,id):
     menu = Mess.objects.filter(id = id)

     context = {
          'Menu': menu,
     }
     return render(request,'owner/update_menu.html',context)


def SAVE_UPDATE_MENU(request):
     if request.method == "POST":
          day_id = request.POST.get('day_id')
          print(day_id)
          day = request.POST.get('day')
          breakfast = request.POST.get('breakfast')
          lunch = request.POST.get('lunch')
          dinner = request.POST.get('dinner')
          print(day_id,day,breakfast,lunch,dinner)

          menu = Mess.objects.get(id = day_id )
          menu.day = day
          menu.breakfast = breakfast
          menu.lunch = lunch
          menu.dinner = dinner

          menu.save()
          messages.success(request,'menu updated successfully')
          return redirect('view_menu')


     return render(request,'owner/update_menu.html')



def DELETE_MENU(request,id):
     menu = Mess.objects.get(id = id )
     menu.delete()
     messages.success(request, 'menu deleted successfully')

     return redirect('view_menu')

def view_list_bill(request):
    # Retrieve all billing records
    billing_records = Billing.objects.all()

    # Render the billing records template
    return render(request, 'staff/view_list_bill.html', {'billing_records': billing_records})
