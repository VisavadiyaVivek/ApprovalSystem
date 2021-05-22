from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from project.models import CustomUser, Guide,HOD,Team, Project,Admin,Student,FeedBackStudent


def guide_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    g_obj = Guide.objects.get(admin=user)
    t_obj = Team.objects.filter(guide_id=g_obj.id)
    total_students=0
    total_projects=0
    for t in t_obj:
        total_students+=Student.objects.filter(team_id=t.id).count()
        total_projects+=Project.objects.filter(p_id=t.p_id.p_id).count()
    
    total_teams = Team.objects.filter(guide_id=g_obj.id).count()
    # total_students = Student.objects.filter(team_id=t_obj.id).count()
    # total_projects = Project.objects.filter(p_id=t_obj.id).count()
    
    context = {
        "total_teams" : total_teams,
        "total_students" : total_students,
        "total_projects" : total_projects,
    }
    return render(request,'project/guide_templates/guide_home.html',context)


def guide_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    g_id = Guide.objects.get(admin=user)
    context = {
        "g_id" : "g_id",
        "user" : user
    }

    return render(request, 'project/guide_templates/guide_profile.html', context)



def guide_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('guide_profile')
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

            guide = Guide.objects.get(admin=customuser.id)
            guide.phone_number = phone_number
            guide.department = department
            guide.save()
            
            messages.success(request, "Guide Updated Successfully")
            return redirect('guide_profile')
        except:
            messages.error(request, "Failed to Update Guide")
            return redirect('guide_profile')



def guide_team_view(request):
    g_obj = Guide.objects.get(admin=request.user.id)
    t_obj_list = g_obj.team_set.all()
    
    st_obj_list = []
    for t in t_obj_list:
        st_obj_list.append(t.student_set.all())
        
    data_list = zip(t_obj_list,st_obj_list)
    context = {
        "data_list" : data_list
    }

    return render(request,'project/guide_templates/guide_team_view.html',context)



def guide_project_view(request,p_id):
   
    p_obj = Project.objects.get(p_id=p_id)
    
    context = {
        "p_obj":p_obj
    }
    return render(request,'project/guide_templates/guide_project_view.html',context)

def guide_project_approved(request,p_id):
    project = Project.objects.get(p_id=p_id)

    project.status = 'Approved By Guide'
    project.save()

    return redirect('/guide_project_view/'+p_id)

def student_detail_view(request,s_id):
    student = Student.objects.get(id=s_id)
    
    context = {
        "student" : student
    }

    return render(request,'project/guide_templates/student_detail_view.html',context)


def guide_student_feedback(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks" : feedbacks
    }

    return render(request, 'project/guide_templates/guide_student_feedback.html',context)


@csrf_exempt
def student_feedback_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")
    

