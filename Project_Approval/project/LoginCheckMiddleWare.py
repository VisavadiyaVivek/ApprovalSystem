from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user

        #Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "project.adminViews":
                    pass
                elif modulename == "project.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("admin_home")
            
            elif user.user_type == "2":
                if modulename == "project.hodViews":
                    pass
                elif modulename == "project.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("hod_home")
            
            elif user.user_type == "3":
                if modulename == "project.guideViews":
                    pass
                elif modulename == "project.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("guide_home")
            
            elif user.user_type == "4":
                if modulename == "project.studentViews":
                    pass
                elif modulename == "project.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("student_home")

            else:
                return redirect("doLogin")

        else:
            if modulename == "project.views" or modulename == "django.contrib.admin.sites" or modulename == "django.contrib.auth.views":
                pass
            elif request.path == reverse("project-home") or request.path == reverse("project-about"):
                pass
            else:
                return redirect("doLogin")