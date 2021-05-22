from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from reportlab.pdfgen import canvas

from project.models import CustomUser, Guide,HOD,Team, Project,Admin,Student,FeedBackStudent
from .forms import EditFileForm,EditStudentFileForm


def student_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    student_obj = Student.objects.get(admin=request.user.id)
    team_obj = Team.objects.get(id=student_obj.team_id.id)
    project_obj = Project.objects.get(p_id=team_obj.p_id.p_id)
    hod_obj = HOD.objects.get(id=team_obj.hod_id.id)
    guide_obj = Guide.objects.get(id = team_obj.guide_id.id)

    team_name = team_obj.name
    student_team_id = team_obj.id
    project_title = project_obj.title
    project_id = project_obj.p_id
    project_status = project_obj.status
    hod_name = hod_obj.admin.first_name + " "+hod_obj.admin.last_name
    guide_name = guide_obj.admin.first_name + " "+guide_obj.admin.last_name


    context = {
        "team_name":team_name,
        "student_team_id":student_team_id,
        "project_title" : project_title,
        "project_id" : project_id,
        "project_status" : project_status,
        "hod_name" : hod_name,
        "guide_name": guide_name
    }
    
    return render(request, 'project/student_templates/student_home.html',context)
    
        


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Student.objects.get(admin=user)

    context = {
        "user" : user,
        "student" : student
    }

    return render(request, 'project/student_templates/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        department = request.POST.get('department')
        enrollment_no = request.POST.get('enrollment_no')
        sem = request.POST.get('sem')
        phon_no = request.POST.get('phon_no')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Student.objects.get(admin=customuser.id)
            student.department = department
            student.sem = sem
            student.enrollment_no = enrollment_no
            student.phon_no = phon_no
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_team_view(request):
    student_obj = Student.objects.get(admin=request.user.id)
    t_id = student_obj.team_id.id
    member_id = Team.objects.get(id=t_id)
    members = Student.objects.filter(team_id=member_id).all()
  
    context = {
        "members" : members
       
    }

    return render(request,'project/student_templates/student_team_view.html',context)


def student_manage_project(request):
    stud_obj = Student.objects.get(admin=request.user.id)
    t_obj = Team.objects.get(id=stud_obj.team_id.id)
    projects = Project.objects.get(p_id=t_obj.p_id.p_id)
    
    context = {
        "projects":projects,
        "t_obj" : t_obj
        
    }
    return render(request, 'project/student_templates/student_manage_project.html', context)

def student_edit_project(request,p_id):
    request.session['p_id'] = p_id

    project = Project.objects.get(p_id = p_id)

    form = EditStudentFileForm()

    form.fields['p_id'].initial = project.p_id
    form.fields['title'].initial = project.title
    form.fields['description'].initial = project.description
    #form.fields['status'].initial = project.status
    
    context = {
        "p_id": p_id,
        "form": form
    }

    return render(request, 'project/student_templates/student_edit_project.html', context)



def student_project_update(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!!")
    else:
        p_id = request.session.get('p_id')
        
        if p_id == None:
            return redirect('/student_manage_project')
        
        form = EditFileForm(request.POST,request.FILES)
        if form.is_valid():
            p_id = form.cleaned_data['p_id']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']

            if(len(request.FILES)!=0):
                report = request.FILES['report']
                fs = FileSystemStorage()
                filename= fs.save(report.name,report)
                report_url = fs.url(filename)
            else:
                report_url = None

            try:
                project_model = Project.objects.get(p_id = p_id)
                project_model.p_id = p_id
                project_model.title = title
                project_model.description = description
                project_model.status  = status
                project_model.report = report_url

                project_model.save()

                del request.session['p_id']

                messages.success(request, "Project Upadated Successfully!!!")
                return redirect('/student_edit_project/'+p_id)
            except:
                messages.error(request, "Failed to Upadate Project!!")
                return redirect('/student_edit_project/'+p_id)
        else:
            messages.error(request,"error")
            return redirect('/student_edit_project/'+p_id)
        

def student_feedback(request):
    student_obj = Student.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'project/student_templates/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Student.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')

