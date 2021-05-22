from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from . import views
from django.contrib.auth import views as auth_views
from . import adminViews, studentViews, guideViews, hodViews


urlpatterns = [
    path('', views.home, name = 'project-home'),
    path('about/', views.about, name = 'project-about'),
    path('doLogin/', views.doLogin, name='doLogin'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('admin_profile/', adminViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', adminViews.admin_profile_update, name="admin_profile_update"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', adminViews.admin_home, name="admin_home"),
    path('check_email_exist/', adminViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', adminViews.check_username_exist, name="check_username_exist"),
    path('manage_student/', adminViews.manage_student, name="manage_student"),
    path('add_student/', adminViews.add_student, name="add_student"),
    path('add_student_save/', adminViews.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', adminViews.edit_student, name="edit_student"),
    path('edit_student_save/', adminViews.edit_student_save, name="edit_student_save"),
    path('manage_student/', adminViews.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', adminViews.delete_student, name="delete_student"),
    path('add_guide/', adminViews.add_guide, name="add_guide"),
    path('add_guide_save/', adminViews.add_guide_save, name="add_guide_save"),
    path('manage_guide', adminViews.manage_guide, name="manage_guide"),
    path('edit_guide/<guide_id>/', adminViews.edit_guide, name="edit_guide"),
    path('edit_guide_save/', adminViews.edit_guide_save, name="edit_guide_save"),
    path('delete_guide/<guide_id>/', adminViews.delete_guide, name="delete_guide"),
    path('add_hod/', adminViews.add_hod, name="add_hod"),
    path('add_hod_save/', adminViews.add_hod_save, name="add_hod_save"),
    path('manage_hod/', adminViews.manage_hod, name="manage_hod"),
    path('edit_hod/<hod_id>/', adminViews.edit_hod, name="edit_hod"),
    path('edit_hod_save/', adminViews.edit_hod_save, name="edit_hod_save"),
    path('delete_hod/<hod_id>/', adminViews.delete_hod, name="delete_hod"),
    path('add_team/', adminViews.add_team, name="add_team"),
    path('add_team_save/', adminViews.add_team_save, name="add_team_save"),
    path('manage_team/', adminViews.manage_team, name="manage_team"),
    path('edit_team/<team_id>/', adminViews.edit_team, name="edit_team"),
    path('edit_team_save/', adminViews.edit_team_save, name="edit_team_save"),
    path('delete_team/<team_id>/', adminViews.delete_team, name="delete_team"),
    path('add_project/', adminViews.add_project, name="add_project"),
    path('add_project_save/', adminViews.add_project_save, name="add_project_save"),
    path('manage_project/', adminViews.manage_project, name="manage_project"),
    path('edit_project/<p_id>/', adminViews.edit_project, name="edit_project"),
    path('edit_project_save/', adminViews.edit_project_save, name="edit_project_save"),
    path('delete_project/<p_id>/', adminViews.delete_project, name="delete_project"),
    path('admin_project_view/<p_id>', adminViews.admin_project_view, name = "admin_project_view"),
    # path('searchList', adminViews.searchList, name="searchList"),

    #Student Views
    path('student_home/', studentViews.student_home, name="student_home"),
    path('student_profile/', studentViews.student_profile, name="student_profile"),
    path('student_profile_update/', studentViews.student_profile_update, name="student_profile_update"),
    path('student_team_view/', studentViews.student_team_view, name="student_team_view"),
    path('student_manage_project/', studentViews.student_manage_project, name="student_manage_project"),
    path('student_edit_project/<p_id>/', studentViews.student_edit_project, name="student_edit_project"),
    path('student_project_update/', studentViews.student_project_update, name="student_project_update"),
    #url(r'^report_upload/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    path('student_feedback/', studentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', studentViews.student_feedback_save, name="student_feedback_save"),
    

    #Guide Views

    path('guide_home/', guideViews.guide_home, name="guide_home"),
    path('guide_profile/', guideViews.guide_profile, name="guide_profile"),
    path('guide_profile_update/', guideViews.guide_profile_update, name="guide_profile_update"),
    path('guide_team_view/', guideViews.guide_team_view, name="guide_team_view"),
    path('guide_project_view/<p_id>', guideViews.guide_project_view, name="guide_project_view"),
    path('guide_student_feedback/', guideViews.guide_student_feedback, name="guide_student_feedback"),
    path('student_feedback_reply/', guideViews.student_feedback_reply, name="student_feedback_reply"),
    path('student_detail_view/<s_id>', guideViews.student_detail_view, name="student_detail_view"),
    path('guide_project_approved/<p_id>', guideViews.guide_project_approved, name="guide_project_approved"),


    #HOD Views
    path('hod_home/', hodViews.hod_home, name="hod_home"),
    path('hod_profile/', hodViews.hod_profile, name="hod_profile"),
    path('hod_profile_update/', hodViews.hod_profile_update, name="hod_profile_update"),
    path('hod_team_view/', hodViews.hod_team_view, name="hod_team_view"),
    path('hod_project_view/<p_id>', hodViews.hod_project_view, name="hod_project_view"),
    path('hod_project_approved/<p_id>', hodViews.hod_project_approved, name="hod_project_approved"),
    path('student_info_view/<s_id>', hodViews.student_info_view, name="student_info_view"),


    #Report Url
    path("report_download/<path>", views.report_download, name="report_download"),

]

