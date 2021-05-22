from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Admin, HOD, Guide, Student, Project, Team, FeedBackStudent, FeedBackHod, FeedBackGuide

# Register your models here.


class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(Admin)
admin.site.register(HOD)
admin.site.register(Guide)
admin.site.register(Student)
admin.site.register(Project)
admin.site.register(Team)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackGuide)
admin.site.register(FeedBackHod)
