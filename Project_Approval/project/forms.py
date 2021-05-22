from django import forms
from django.forms import Form
from .models import Team


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    phon_no = forms.CharField(label="Phone No", max_length=12, widget=forms.TextInput(attrs={"class":"form-control"}))
    department = forms.CharField(label="Department", max_length=10, widget=forms.TextInput(attrs={"class":"form-control"}))
    enrollment_no = forms.CharField(label="Enrollment No", max_length=20, widget=forms.TextInput(attrs={"class":"form-control"}))
      
    try:
        teams = Team.objects.all()
        team_list = []
        for t in teams:
            single_team = (t.id, t.name)
            team_list.append(single_team)
    except:
        team_list = []

    leader_list = (('NO','NO'),('YES','YES'))
    sem_list = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'))

    sem = forms.ChoiceField(label="Semester", choices=sem_list, widget=forms.Select(attrs={"class":"form-control"}))
    leader = forms.ChoiceField(label="Leader", choices=leader_list, widget=forms.Select(attrs={"class":"form-control"}))
    team_id = forms.ChoiceField(label = "Team", choices=team_list, widget = forms.Select(attrs={"class":"form-control"}))
    


class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    phon_no = forms.CharField(label="Phone No", max_length=12, widget=forms.TextInput(attrs={"class":"form-control"}))
    department = forms.CharField(label="Department", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    enrollment_no = forms.CharField(label="Enrollment No", max_length=20, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    
    try:
        teams = Team.objects.all()
        team_list = []
        for team in teams:
            single_team = (team.id, team.name)
            team_list.append(single_team)
    except:
        team_list = []
    
    leader_list = (('No','No'),('Yes','Yes'))
    sem_list = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'))

    sem = forms.ChoiceField(label="Semester", choices=sem_list, widget=forms.Select(attrs={"class":"form-control"}))
    leader = forms.ChoiceField(label="Leader", choices=leader_list, widget=forms.Select(attrs={"class":"form-control"}))
    team_id = forms.ChoiceField(label = "Team", choices=team_list, widget = forms.Select(attrs={"class":"form-control"}))
    

class AddFileForm(forms.Form):

    p_id = forms.CharField(label="Project Id", max_length=20, widget=forms.TextInput(attrs = {"class":"form-control"}))
    title = forms.CharField(label="Title", max_length=50, widget=forms.TextInput(attrs = {"class":"form-control"}))
    description = forms.CharField(label="Description", max_length=500, widget=forms.TextInput(attrs = {"class":"form-control"}))

    status_list = (('not_assigned','Not Assigned'),
    ('assigned', 'Assigned'),
    ('on_going', 'On Going'),
    ('completed' , 'Completed'),
    ('approved_by_guide' ,'Approved By Guide'),
    ('approved_by_hod' , 'Approved By Hod'))

    status = forms.ChoiceField(label="Project Status",choices = status_list, widget=forms.Select(attrs = {"class":"form-control"}))
    report = forms.FileField(label = "Project Report", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))


class EditFileForm(forms.Form):

    p_id = forms.CharField(label="Project Id", max_length=20, widget=forms.TextInput(attrs = {"class":"form-control"}))
    title = forms.CharField(label="Title", max_length=50, widget=forms.TextInput(attrs = {"class":"form-control"}))
    description = forms.CharField(label="Description", max_length=500, widget=forms.TextInput(attrs = {"class":"form-control"}))

    status_list = (('not_assigned','Not Assigned'),
    ('assigned', 'Assigned'),
    ('on_going', 'On Going'),
    ('completed' , 'Completed'),
    ('approved_by_guide' ,'Approved By Guide'),
    ('approved_by_hod' , 'Approved By Hod'))

    status = forms.ChoiceField(label="Project Status", choices = status_list, widget=forms.Select(attrs = {"class":"form-control"}))
    report = forms.FileField(label = "Project Report", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))


class EditStudentFileForm(forms.Form):
    p_id = forms.CharField(label="Project Id", max_length=20, widget=forms.TextInput(attrs = {"class":"form-control"}))
    title = forms.CharField(label="Title", max_length=50, widget=forms.TextInput(attrs = {"class":"form-control"}))
    description = forms.CharField(label="Description", max_length=500, widget=forms.TextInput(attrs = {"class":"form-control"}))

    status_list = (
    ('assigned', 'Assigned'),
    ('on_going', 'On Going'),
    ('completed' , 'Completed'),
    )

    status = forms.ChoiceField(label="Project Status", choices = status_list, widget=forms.Select(attrs = {"class":"form-control"}))
    report = forms.FileField(label = "Project Report", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
