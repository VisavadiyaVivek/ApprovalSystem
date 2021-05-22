from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Reports
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q


from project.models import CustomUser, Admin, HOD, Guide, Project, Student, Team, FeedBackGuide,FeedBackHod, FeedBackStudent
from .forms import AddStudentForm, EditStudentForm, AddFileForm, EditFileForm


def admin_home(request):
    
    all_student_count = Student.objects.all().count()
    project_count = Project.objects.all().count()
    guide_count = Guide.objects.all().count()
    hod_count = HOD.objects.all().count()
    team_count = Team.objects.all().count()

    student_name_list = []
    students = Student.objects.all()
    for student in students:
        student_name_list.append(student.admin.first_name)


    total_list = Project.objects.all()

    project_list=[]

    for l in total_list:
        if l.status == "Approved By HOD":
            project_list.append(l)
    

    guide_name_list = []
    guide_list = Guide.objects.all()
    for g in guide_list:
        guide_name_list.append(g.admin.first_name)

    hod_name_list = []
    hod_list = HOD.objects.all()
    for h in hod_list:
        hod_name_list.append(h.admin.first_name)

    team_name_list = []
    team_list = Team.objects.all()
    for t in team_list:
        team_name_list.append(t.name)
    

    context = {
        'all_student_count':all_student_count,
        'project_count':project_count,
        'guide_count':guide_count,
        'hod_count':hod_count,
        'team_count':team_count,
        'team_name_list':team_name_list,
        'student_name_list':student_name_list,
        'project_list':project_list,
        'guide_name_list':guide_name_list,
        'hod_name_list':hod_name_list,
    }

    return render(request, 'project/admin_templates/admin_home.html',context)


def manage_student(request):
    students = Student.objects.all()
    query = request.GET.get('query')
    if query:
        query = query.split()
        if len(query) == 2:
            students = students.filter(admin__first_name__contains=query[0] , admin__last_name__contains= query[1])  
        else:
            students = students.filter(Q(admin__first_name__contains=query[0])
             | Q(admin__last_name__contains = query[0])
             | Q(enrollment_no__contains = query[0]))
    
    context = {
        "students": students
    }
    return render(request, 'project/admin_templates/manage_student.html', context)


def add_student(request):
    form = AddStudentForm()
    teams = Team.objects.all()
    context = {
        "form":form,
        "teams":teams
    }
    return render(request, 'project/admin_templates/add_student.html',context)


def add_student_save(request):
    if request.method != 'POST':
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            department = form.cleaned_data['department']
            enrollment_no = form.cleaned_data['enrollment_no']
            team_id = form.cleaned_data['team_id']
            phon_no = form.cleaned_data['phon_no']          
            sem = form.cleaned_data['sem']
            team_id = form.cleaned_data['team_id']
            leader = form.cleaned_data['leader']

            try: 
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=4)
                user.student.department = department

                team_obj = Team.objects.get(id=team_id)
                user.student.team_id = team_obj
                user.student.sem = sem
                user.student.enrollment_no = enrollment_no
                user.student.leader = leader
                user.student.phon_no = phon_no
                    
                user.save()
                messages.success(request, "Student Added Successfully!!!")
                return redirect('add_student')
            except:
                messages.error(request, "Failed to Add Student!!!")
                return redirect('add_student')

        else:
            return redirect('add_student')
        
        
        

def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Student.objects.get(admin=student_id)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['department'].initial = student.department
    form.fields['enrollment_no'].initial = student.enrollment_no
    form.fields['team_id'].initial = student.team_id.id
    form.fields['leader'].initial = student.leader
    form.fields['phon_no'].initial = student.phon_no
    form.fields['sem'].initial = student.sem

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "project/admin_templates/edit_student.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            department = form.cleaned_data['department']
            enrollment_no = form.cleaned_data['enrollment_no']
            team_id = form.cleaned_data['team_id']
            leader = form.cleaned_data['leader']
            sem = form.cleaned_data['sem']
            phon_no = form.cleaned_data['phon_no']


            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
           

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Student.objects.get(admin=student_id)
                student_model.department = department
                team = Team.objects.get(id=team_id)
                student_model.team_id = team               
                student_model.enrollment_no = enrollment_no
                student_model.gender = leader
                student_model.sem = sem
                student_model.phon_no = phon_no
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except:
                messages.error(request, "Failed to Add Student.")
                return redirect('/edit_student/'+student_id)
        else:
            return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
    student = Student.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_guide(request):
    return render(request, "project/admin_templates/add_guide.html")


def add_guide_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_guide')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        department = request.POST.get('department')
        phone_number = request.POST.get('phone_number')
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.guide.department = department
            user.guide.phone_number = phone_number
            user.save()
            messages.success(request, "Guide Added Successfully!!!")
            return redirect('add_guide')
        except:
            messages.error(request, "Failed to Add Guide!!")
            return redirect('add_guide')
        



def manage_guide(request):
    guides = Guide.objects.all()
    
    query = request.GET.get('query')
    if query:
        query = query.split()
        if len(query) == 2:
            guides = guides.filter(admin__first_name__contains=query[0] , admin__last_name__contains= query[1])  
        else:
            guides = guides.filter(Q(admin__first_name__contains=query[0]) | Q(admin__last_name__contains = query[0]))
    context = {
        "guides": guides
    }
    return render(request, "project/admin_templates/manage_guide.html", context)


def edit_guide(request, guide_id):
    guide = Guide.objects.get(admin=guide_id)

    context = {
        "guide": guide,
        "id": guide_id
    }
    return render(request, "project/admin_templates/edit_guide.html", context)


def edit_guide_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        guide_id = request.POST.get('guide_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department = request.POST.get('department')
        phone_number = request.POST.get('phone_number')


        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=guide_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into Staff Model
            guide_model = Guide.objects.get(admin=guide_id)
            guide_model.department = department
            guide_model.phone_number = phone_number
            guide_model.save()

            messages.success(request, "Guide Updated Successfully.")
            return redirect('/edit_guide/'+guide_id)

        except:
            messages.error(request, "Failed to Update Guide.")
            return redirect('/edit_guide/'+guide_id)



def delete_guide(request, guide_id):
    guide = Guide.objects.get(admin=guide_id)
    try:
        guide.delete()
        messages.success(request, "Guide Deleted Successfully.")
        return redirect('manage_guide')
    except:
        messages.error(request, "Failed to Delete Guide.")
        return redirect('manage_guide')


def add_hod(request):
    return render(request, "project/admin_templates/add_hod.html")


def add_hod_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_hod')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        department = request.POST.get('department')
        phone_number = request.POST.get('phone_number')
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.hod.department = department
            user.hod.phone_number = phone_number
            user.save()
            messages.success(request, "HOD Added Successfully!!!")
            return redirect('add_hod')
        except:
            messages.error(request, "Failed to Add HOD!!")
            return redirect('add_hod')
        



def manage_hod(request):
    hods = HOD.objects.all()
    query = request.GET.get('query')
    if query:
        query = query.split()
        if len(query) == 2:
            hods = hods.filter(admin__first_name__contains=query[0] , admin__last_name__contains= query[1])  
        else:
            hods = hods.filter(Q(admin__first_name__contains=query[0]) | Q(admin__last_name__contains = query[0]))
    
    context = {
        "hods": hods
    }
    return render(request, "project/admin_templates/manage_hod.html", context)


def edit_hod(request, hod_id):
    hod = HOD.objects.get(admin=hod_id)

    context = {
        "hod": hod,
        "id": hod_id
    }
    return render(request, "project/admin_templates/edit_hod.html", context)


def edit_hod_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        hod_id = request.POST.get('hod_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department = request.POST.get('department')
        phone_number = request.POST.get('phone_number')


        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=hod_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into Staff Model
            hod_model = HOD.objects.get(admin=hod_id)
            hod_model.department = department
            hod_model.phone_number = phone_number
            hod_model.save()

            messages.success(request, "HOD Updated Successfully.")
            return redirect('/edit_hod/'+hod_id)

        except:
            messages.error(request, "Failed to Update HOD!!.")
            return redirect('/edit_hod/'+hod_id)



def delete_hod(request, hod_id):
    hod = HOD.objects.get(admin=hod_id)
    try:
        hod.delete()
        messages.success(request, "HOD Deleted Successfully.")
        return redirect('manage_hod')
    except:
        messages.error(request, "Failed to Delete HOD.")
        return redirect('manage_hod')


def add_team(request):
    projects = Project.objects.all()
    guides = Guide.objects.all()
    hods = HOD.objects.all()
    context = {
        "projects" : projects,
        "guides" : guides,
        "hods" : hods
    }
    return render(request, 'project/admin_templates/add_team.html',context)

def add_team_save(request):
    if request.method!="POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_team')
    else:
        name = request.POST.get('name')
        p_id = request.POST.get('p_id')
        project = Project.objects.get(id = p_id)

        g_id = request.POST.get('guide_id')
        guide = Guide.objects.get(id = g_id)
        
        h_id = request.POST.get('hod_id')
        hod = HOD.objects.get(id = h_id)

        
        team = Team(name=name, p_id = project, guide_id = guide, hod_id = hod)
        team.save()
        messages.success(request, "Team Added Successfully!")
        return redirect('add_team')
        

def manage_team(request):
    teams = Team.objects.all()
    query = request.GET.get('query')
    if query:
        teams = teams.filter(Q(name__contains=query) | Q(p_id_id__title__contains = query)
                 | Q(guide_id_id__admin__first_name__contains = query)
                 | Q(hod_id_id__admin__first_name__contains = query))
    
    context = {
        "teams":teams
    }
    return render(request,'project/admin_templates/manage_team.html',context)

def edit_team(request, team_id):
    team = Team.objects.get(id=team_id)
    guides = Guide.objects.all()
    hods = HOD.objects.all()
    projects = Project.objects.all()

    context={
        "team": team,
        "prpjects": projects,
        "guides" : guides,
        "hods" : hods
    }   
    return render(request, 'project/admin_templates/edit_team.html',context)

def edit_team_save(request):

    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        team_id = request.POST.get('team_id')
        if team_id == None:
            return redirect('manage_team')

        team_name = request.POST.get('name')
        p_id = request.POST.get('p_id')
        guide_id = request.POST.get('guide_id')
        hod_id = request.POST.get('hod_id')

        try:
            team = Team.objects.get(id=team_id)
            team.name = team_name
            project_obj = Project.objects.get(p_id=p_id)
            team.project_id=project_obj
            guide_obj = Guide.objects.get(id=guide_id)
            team.guide_id = guide_obj
            hod_obj = HOD.objects.get(id=hod_id)
            team.hod_id = hod_obj
            team.save()
            messages.success(request, "Team Updated Successfully.")
            return HttpResponseRedirect(reverse('edit_team', kwargs={'team_id':team_id}))

        except:
            messages.error(request, "Failed to Update Team.")
            return HttpResponseRedirect(reverse('edit_team', kwargs={'team_id':team_id}))
            

def delete_team(request,team_id):
    team = Team.objects.get(id = team_id)
    try:
        team.delete()
        messages.success(request, "Team Deleted Successfully.")
        return redirect('manage_team')
    except:
        messages.error(request, "Failed to Delete Team.")
        return redirect('manage_team')


def add_project(request):
    form = AddFileForm()
    context = {
        "form" : form
    }
    return render(request, 'project/admin_templates/add_project.html',context)


def add_project_save(request):

    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_project')
    else:
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            p_id = form.cleaned_data['p_id']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']

            if(len(request.FILES) != 0):
                report = request.FILES['report']
                fs = FileSystemStorage()
                filename = fs.save(report.name,report)
                report_url = fs.url(filename)
            else:
                report_url = None

            try:
                project = Project(p_id = p_id, title = title, description = description, status = status, report = report_url)
                project.save()
                messages.success(request, "Project Added Successfully!")
                return redirect('add_project')
            except:
                messages.error(request, "Failed to Add Project!!!")
                return redirect('add_project')

            

def manage_project(request):
    projects = Project.objects.all()
    query = request.GET.get('query')
    if query:
        projects = projects.filter(Q(title__contains=query) | Q(p_id__contains = query))
                 
    context = {
        "projects":projects
    }
    return render(request, 'project/admin_templates/manage_project.html', context)


def edit_project(request, p_id):

    request.session['p_id'] = p_id

    project = Project.objects.get(p_id = p_id)

    form = EditFileForm()

    form.fields['p_id'].initial = project.p_id
    form.fields['title'].initial = project.title
    form.fields['description'].initial = project.description
    form.fields['status'].initial = project.status
    
    context = {
        "p_id": p_id,
        "form": form
    }

    return render(request, 'project/admin_templates/edit_project.html', context)

def edit_project_save(request):

    if request.method != "POST":
        return HttpResponse("Invalid Method!!")
    else:
        p_id = request.session.get('p_id')
        if p_id == None:
            return redirect('/manage_project')
        
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
                return redirect('/edit_project/'+p_id)
            except:
                messages.error(request, "Failed to Upadate Project!!")
                return redirect('/edit_project/'+p_id)
        else:
            return redirect('/edit_project/'+p_id)


def delete_project(request, p_id):
    pro = Project.objects.get(p_id=p_id)

    try:
        pro.delete()
        messages.success(request, "Project Deleted Successfully!!")
        return redirect('manage_project')
    except:
        messages.error(request, "Falied to Delete Project!!!")
        return redirect('manage_project')

def admin_project_view(request,p_id):
    p_obj = Project.objects.get(p_id=p_id)

    context = {
        'p_obj': p_obj
    }

    return render(request,'project/admin_templates/admin_project_view.html',context)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user":user
    }

    return render(request, 'project/admin_templates/admin_profile.html',context)

def admin_profile_update(request):
    if request.method != 'POST':
        messages.error(request, "Invalid Method!!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')




def guide_profile(request):
    pass

def hod_profile(request):
    pass

def student_profile(request):
    pass


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


