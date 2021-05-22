from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from project.EmailBackEnd import EmailBackEnd

# Create your views here.
def home(request):

    return render(request, 'project/home.html')

def about(request):

    return render(request, 'project/about.html')

def doLogin(request):
    if request.method != 'POST':
        return render(request, 'project/login.html')
    else:
        
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password = request.POST.get('password'))

        if user != None:
            login(request, user)
            user_type = user.user_type


            if user_type == '1':
                return redirect('admin_home')
            elif user_type == '2':
                return redirect('hod_home')
            elif user_type == '3':
                return redirect('guide_home')
            elif user_type == '4':
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!!!")
                return redirect('doLogin')
        else:
            messages.error(request, "Invalid Login Credentials!!!")
            return redirect('doLogin')    


def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def report_download(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb') as fh:
            response = HttpResponse(fh.read(),content_type="application/report")
            response['Content-Disposition']='attachment; filename='+os.path.basename(file_path)
            return response
    else:
        raise Http404


def sending_email(request):
    if request.method == "POST":
        to = request.POST.get('email')
        send_mail("Password Reset Email",
        "Message",
        settings.EMAIL_HOST_USER,
        [to]  
        )
        return render(request,'accounts/password_reset_done.html')
    else:
        return render(request,'project/password_reset.html')

    
