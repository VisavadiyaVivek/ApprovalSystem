from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse

from project.models import CustomUser, Guide,HOD,Team, Project,Admin,Student


def hod_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    h_obj = HOD.objects.get(admin=user)
    t_obj = Team.objects.filter(hod_id=h_obj.id)
    total_students=0
    total_projects=0
    for t in t_obj:
        total_students+=Student.objects.filter(team_id=t.id).count()
        total_projects+=Project.objects.filter(p_id=t.p_id.p_id).count()
    
    total_teams = Team.objects.filter(guide_id=h_obj.id).count()
    # total_students = Student.objects.filter(team_id=t_obj.id).count()
    # total_projects = Project.objects.filter(p_id=t_obj.id).count()
    
    context = {
        "total_teams" : total_teams,
        "total_students" : total_students,
        "total_projects" : total_projects,
    }
    return render(request,'project/hod_templates/hod_home.html',context)


def hod_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    h_obj = HOD.objects.get(admin=user)
    context = {
        "h_obj" :  h_obj,
        "user" : user
    }

    return render(request, 'project/hod_templates/hod_profile.html', context)



def hod_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('hod_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        department = request.POST.get('department')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            hod = HOD.objects.get(admin=customuser.id)
            hod.phone_number = phone_number
            hod.department = department
            hod.save()
            
            messages.success(request, "HOD Updated Successfully!!!")
            return redirect('hod_profile')
        except:
            messages.error(request, "Failed to Update HOD!!!")
            return redirect('hod_profile')



def hod_team_view(request):
    h_obj = HOD.objects.get(admin=request.user.id)
    t_obj_list = h_obj.team_set.all()
    
    st_obj_list = []
    for t in t_obj_list:
        st_obj_list.append(t.student_set.all())
        
    data_list = zip(t_obj_list,st_obj_list)
    context = {
        "data_list" : data_list
    }

    return render(request,'project/hod_templates/hod_team_view.html',context)


def student_info_view(request,s_id):
    student = Student.objects.get(id=s_id)
    context = {
        'student' : student
    }

    return render(request,'project/hod_templates/student_info_view.html',context)




def hod_project_view(request,p_id):
   
    p_obj = Project.objects.get(p_id=p_id)
    
    context = {
        "p_obj":p_obj
    }
    return render(request,'project/hod_templates/hod_project_view.html',context)


def hod_project_approved(request,p_id):
    project = Project.objects.get(p_id=p_id)

    project.status = 'Approved By HOD'
    project.save()

    return redirect('/hod_project_view/'+p_id)