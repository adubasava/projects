from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.core.exceptions import PermissionDenied
from django.db.models import Max 
from django.db.models import F

from .models import User, Course, Group, Student, Enroll


def index(request):    
    return render(request, "school/index.html")

# Teacher's profile
@login_required
def tprofile(request, id):
    user = User.objects.get(pk=id)
    courses = Course.objects.filter(user=user)
    return render(request, "school/tprofile.html", {
        "courses": courses,
        "user": user,
    })


# Teacher's courses (for teachers only)
@login_required
def courses(request):
    user = request.user
    if user.role == User.TEACHER:
        courses = Course.objects.filter(user=request.user)
        return render(request, "school/courses.html", {
            "courses": courses,
        })
    else:
        raise PermissionDenied()


# Add a new course (for teachers only)
@login_required
def create(request):
    courses = Course.objects.filter(user=request.user)
    if request.method == "POST":          
        course = Course(
            user=request.user,
            title=request.POST["title"],
            description=request.POST["description"],
            level=request.POST["level"],
            hours=request.POST["hours"],
        )
        course.save()
        return HttpResponseRedirect(reverse('courses'))

    return render(request, "school/courses.html", {
            "courses": courses,
        })


# Remove course (for teachers only)
@csrf_exempt
@login_required
def remove_course(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    id = data.get("id", "")
    course = Course.objects.get(pk=id)    
    course.delete()
    
    return JsonResponse({"message": "Course deleted successfully.", id:id}, status=201)


# Add student into course group (for teachers only)
@csrf_exempt
@login_required
def add_student(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)    
    id = data.get("id", "")
    group = Group.objects.get(pk=id)
    user_id = data.get("user", "")
    user = User.objects.get(pk=user_id)

    # Check if student is not already added
    if Student.objects.filter(user=user,group=group):
        return JsonResponse({"message": "Student alredy added."}, status=201)
    
    student = Student(
            user=user,
            group=group,
        )
    student.save()

    # Update students count in the group
    group.stud_current = group.stud_current + 1
    group.save()
    
    return JsonResponse({"message": "Student added successfully."}, status=201)


# Remove student from course group (for teachers only)
@csrf_exempt
@login_required
def remove_student(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    id = data.get("id", "")
    student = Student.objects.get(pk=id)
    group = Group.objects.get(pk=student.group.id)    
    student.delete()

    # Update students count in the group
    group.stud_current = group.stud_current - 1
    group.save()

    return JsonResponse({"message": "Student removed from the course successfully."}, status=201)


# Edit course (for teachers only)
@csrf_exempt
@login_required
def edit_course(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    
    id = data.get("id", "")
    title = data.get("title", "")
    level = data.get("level", "")
    hours = data.get("hours", "")
    description = data.get("description", "")

    # Edit course
    course = Course.objects.get(pk=id)
    course.title = title
    course.level = level
    course.hours = hours
    course.description = description
    course.save()
    return JsonResponse({"message": "Course updated successfully."}, status=201)


# Course page 
@login_required
def course(request, id):    
    course = Course.objects.get(pk=id)
    groups = Group.objects.filter(course=course)

    # Check if the course is open for registration ( 0 means it is closed)
    try:
        enroll = Enroll.objects.get(course=course)
    except:
        enroll = 0  
    
    return render(request, "school/course.html" , {
            "course": course,
            "groups": groups,
            "enroll": enroll,
    })


@csrf_exempt
@login_required
# Close registration (for teachers only)
def close(request):    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    id = data.get("id", "")
    enroll = Enroll.objects.get(course=id)    
    enroll.delete()

    return JsonResponse({"message": "Registration closed."}, status=201)


@csrf_exempt
@login_required
# Open registration (for teachers only)
def open(request):    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    id = data.get("id", "")

    # As most fields in the form are optional, convert empty fields into None
    enroll_start = data.get("enroll_start", "")
    if enroll_start == '':
        enroll_start = None

    enroll_end = data.get("enroll_end", "")
    if enroll_end == '':
        enroll_end = None

    course_start = data.get("course_start", "")
    if course_start == '':
        course_start = None

    course_end = data.get("course_end", "")
    if course_end == '':
        course_end = None

    stud_min = data.get("stud_min", "")
    if stud_min == '':
        stud_min = None

    stud_max = data.get("stud_max", "")
    if stud_max == '':
        stud_max = None

    gr = data.get("gr", "")
    course = Course.objects.get(pk=id)

    # Open course for registration
    enroll = Enroll(
             course=course,
             enroll_start=enroll_start,
             enroll_end=enroll_end,
             course_start=course_start,
             course_end=course_end,
             stud_min=stud_min,
             stud_max=stud_max,
    )
    enroll.save() 
    
    # Add groups into opened course
    for g in gr:
        enroll.group.add(g)         
    enroll.save() 

    return JsonResponse({"message": "Registration opened."}, status=201)


@csrf_exempt
@login_required
# Add new groups to the course opened for registration (for teachers only)
def add_group_enroll(request):    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    id = data.get("id", "")
    gr = data.get("gr", "")
    enroll = Enroll.objects.get(pk=id) 
    
    # Checks if groups were selected (= user has not submitted empty form)
    if len(gr) > 0:
        for g in gr:
            enroll.group.add(g)         
        enroll.save() 

    return JsonResponse({"message": "Group added if not empty."}, status=201)


# Course group page
@login_required
def group(request, id):    
    group = Group.objects.get(pk=id)

    # Course the group belongs
    course = group.course

    # All students
    all = []
    all_students = User.objects.filter(role=User.STUDENT)
    for all_st in all_students:
        all.append(all_st.username)
    
    # Students already enrolled in the course
    enrolled = []
    students = Student.objects.filter(group=group)
    for stud in students:
        enrolled.append(stud.user.username)

    # Unenrolled students
    unenrolled = []
    if len(all) == len(enrolled):
        unenroll = []
    else:
        for st in all:
            if st not in enrolled:
                unenrolled.append(st)
        unenroll = User.objects.filter(role=User.STUDENT,username__in=unenrolled)

    return render(request, "school/group.html" , {
            "group": group,
            "course": course,
            "students": students,
            "all_students": all_students,
            "unenroll": unenroll,
    })


@csrf_exempt
@login_required
# Add group (for teachers only)
def add_gr(request):   
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)    
    id = data.get("id", "")
    title = data.get("title", "")
    course = Course.objects.get(pk=id)

    # Check if title was provided
    if title == '':
        return JsonResponse({"message": "Empty title."}, status=201)
    
    # Check if group with the provided title already exists
    if Group.objects.filter(title=title,teacher=request.user,course=course):
        return JsonResponse({"message": "Group alredy exists."}, status=201)
    
    # Add a group
    group = Group(
                title=title,
                teacher=request.user,
                course=course,
            )
    group.save()        
        
    return JsonResponse({"message": "Group added successfully."}, status=201)


# Remove course group (for teachers only)
@csrf_exempt
@login_required
def remove_group(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    id = data.get("id", "")
    group = Group.objects.get(pk=id)    
    group.delete()

    return JsonResponse({"message": "Group removed successfully."}, status=201)


# Edit course group (for teachers only)
@csrf_exempt
@login_required
def edit_group(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    id = data.get("id", "")
    gtitle = data.get("gtitle", "")
    group = Group.objects.get(pk=id)
    course = Course.objects.get(pk=group.course.id)
    
    # Check if title was provided
    if gtitle == '':
        group(id)
    
    # Check if group with the provided title already exists
    if Group.objects.filter(title=gtitle,teacher=request.user,course=course):
        group(id)

    group.title = gtitle    
    group.save()

    return JsonResponse({"message": "Group edited successfully."}, status=201)


# Student's profile page
@login_required
def stprofile(request, id):
    user = User.objects.get(pk=id)
    student = Student.objects.filter(user=user)
    return render(request, "school/stprofile.html", {
        "student": student,
        "user": user,
    })


# Courses opened for registration
@csrf_exempt
@login_required
def enroll(request):
    # All open registrations
    enroll = Enroll.objects.all()
    
    # Check if student is already registered for the course (to not display such a course on the page)
    courses = []
    for e in enroll:
        for g in e.group.all():
            if Student.objects.filter(user=request.user,group=g.id):                
                grt = g.course.id
                courses.append(grt)

    # Courses student is not enrolled in yet
    enroll = Enroll.objects.exclude(course__in=courses)    

    groups = Group.objects.all()

    # Register for the course
    if request.method == "PUT":  

        data = json.loads(request.body)            
        id = data.get("id", "")

        # Check if student did not submit empty form
        if id == "":
            return JsonResponse({"message": "No groups."}, status=201)
            
        group = Group.objects.get(pk=id)
        user = request.user

        student = Student(
                user=user,
                group=group,
            )
        student.save()

        # Update number of students in the group
        group.stud_current = group.stud_current + 1
        group.save()
            
        return JsonResponse({"message": "Student added successfully."}, status=201)
    
    # Sort results
    if request.method == "POST":    
       
        sort_choice = request.POST.get('sort')
        if sort_choice == "popular":
            enroll = enroll.annotate(stud_current=Max("group__stud_current")).order_by(F("stud_current").desc(nulls_last=True))
        elif sort_choice == "title":
            enroll =  enroll.order_by('course__title')
        elif sort_choice == "instructor":
            enroll =  enroll.order_by('course__user__last_name')
        else:
            enroll =  enroll.order_by(F('course_start').asc(nulls_last=True))

    return render(request, "school/enroll.html", {
        "enroll": enroll,
        "courses": courses,
        "groups": groups,
    })


# Login, logout, register
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "school/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "school/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# + fields for user role, first name and last name
def register(request):
    if request.method == "POST":
        first_name = request.POST["first"]
        last_name = request.POST["last"]
        username = request.POST["username"]
        email = request.POST["email"]
        role = request.POST["role"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "school/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
            # Add user's role, first name, last name
            user.role = role
            user.first_name = first_name.title()
            user.last_name = last_name.title()
            user.save()
        except IntegrityError:
            return render(request, "school/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "school/register.html")
