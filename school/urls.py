from django.urls import path

from . import views

urlpatterns = [
    # For all users
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # For teachers
    path("tprofile<int:id>", views.tprofile, name="tprofile"),  
    path("courses", views.courses, name="courses"),
    path("course/<int:id>", views.course, name="course"),    
    path("create", views.create, name="create"),
    path("group/<int:id>", views.group, name="group"),   

    path("remove_course", views.remove_course, name="remove_course"),
    path("edit_course", views.edit_course, name="edit_course"),
    path("add_gr", views.add_gr, name="add_gr"),
    path("remove_group", views.remove_group, name="remove_group"),
    path("edit_group", views.edit_group, name="edit_group"),
    path("add_student", views.add_student, name="add_student"),
    path("remove_student", views.remove_student, name="remove_student"),
    path("close", views.close, name="close"),
    path("open", views.open, name="open"),
    path("add_group_enroll", views.add_group_enroll, name="add_group_enroll"),

    #For students
    path("stprofile<int:id>", views.stprofile, name="stprofile"),  
    path("enroll", views.enroll, name="enroll"),  
]