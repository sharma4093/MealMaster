from django.shortcuts import render,redirect,HttpResponse
from app.emailbackend import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import Customeruser



def BASE(request):
    return render(request, 'base.html')

def LOGIN(request):
    return render(request, 'login.html')
def LOGIN1(request):
    return render(request, 'login_student.html')
def LOGIN2(request):
    return render(request, 'login_staff.html')
  

def MAIN(request):
    return render(request, 'homemain.html')

def doLogin(request):
    if request.method =='POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user!=None:
            login(request,user)
            user_type=user.user_type
            if user_type == '1':
                return redirect( 'owner_home')
            elif user_type =='2':
                 return redirect('staff_home')
            elif user_type =='3':
                 return redirect('student_home')
            else:
                messages.error(request, 'email and password are invalid')
                return redirect('login')
        else:
            messages.error(request, 'email and password are invalid')
            return redirect('login')


def  doLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def PROFILE(request):
    user = Customeruser.objects.get(id = request.user.id)

    context ={
        "user":user,
    }
    return render(request,'profile.html',context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        #email = request.POST.get('email')
        #username = request.POST.get('username')
        password = request.POST.get('password')
        print(profile_pic,first_name,last_name)

        try: 
            Customer_user = Customeruser.objects.get(id = request.user.id)
            Customer_user.first_name = first_name
            Customer_user.last_name = last_name

            if password != None and password != "":
                Customer_user.set_password(password)

            if profile_pic != None and profile_pic != "":
                Customer_user.profile_pic = profile_pic
            Customer_user.save()

            messages.success(request, 'your profile updated successfully!! ')
            return redirect('profile')

        except:

            messages.error(request, 'failded to update')
    return render(request,'profile.html')






