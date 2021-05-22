from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1, 'Admin'), (2, 'HOD'), (3, 'Guide'), (4, 'Student'))
    user_type = models.CharField(default = 1, choices = user_type_data, max_length = 10)

    def save(self, **kwargs):
        super(CustomUser,self).save(**kwargs)
        

class Admin(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, on_delete= models.CASCADE)
    objects = models.Manager()

class HOD(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, on_delete= models.CASCADE)
    phone_number = models.CharField(max_length=15)
    department = models.CharField(max_length=20)
    objects = models.Manager()

class Guide(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, on_delete= models.CASCADE)
    phone_number = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    objects = models.Manager()

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    p_id = models.CharField(max_length=20, null = False, unique=True)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    report = models.FileField(upload_to='project_reports', null=True)
    status = models.CharField(max_length=20, null = False)
    objects = models.Manager()

class Team(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=20, null=False)
    p_id = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    guide_id = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True)
    hod_id = models.ForeignKey(HOD, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()



class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete= models.CASCADE)
    phon_no = models.CharField(max_length=12, null=False)
    enrollment_no = models.CharField(max_length=20, null=False)
    sem = models.CharField(max_length=2, null=False)
    team_id = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    department = models.CharField(max_length=20, null=False)
    leader = models.CharField(max_length=10, null=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackGuide(models.Model):
    id = models.AutoField(primary_key=True)
    guide_id = models.ForeignKey(Guide, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackHod(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(HOD, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    


@receiver(post_save, sender = CustomUser)
def create_user_profile(sender, instance,created,**kwargs):

    if created:

        if instance.user_type == 1:
            Admin.objects.create(admin = instance)
        if instance.user_type == 2:
            HOD.objects.create(admin = instance, phone_number="", department="")
        if instance.user_type == 3:
            Guide.objects.create(admin = instance, phone_number="", department="")
        if instance.user_type == 4:
            Student.objects.create(admin = instance, team_id =Team.objects.get(id=1),leader = "", department = "",enrollment_no= "", sem = "", phon_no = "")


@receiver(post_save, sender = CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.hod.save()
    if instance.user_type == 3:
        instance.guide.save()
    if instance.user_type == 4:
        instance.student.save()

