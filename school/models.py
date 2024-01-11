from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    TEACHER = 1
    STUDENT = 2

    ROLE_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="course_teacher")
    title = models.CharField(max_length = 64)
    description = models.TextField()
    level = models.CharField(max_length = 32)
    hours = models.IntegerField()

    def __str__(self):
        return f"{self.title} ({self.level}) by {self.user.first_name} {self.user.last_name}"

class Group(models.Model):
    title = models.CharField(max_length = 32)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="group_teacher")    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name="course_group")
    stud_current = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.course}, {self.title}"

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="student")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name="group")

    def __str__(self):
        return f"{self.user}, {self.group}"
  
class Enroll(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name="open_course")
    group = models.ManyToManyField(Group, blank=True)
    enroll_start = models.DateField(blank=True, null=True)
    enroll_end = models.DateField(blank=True, null=True)
    course_start = models.DateField(blank=True, null=True)
    course_end = models.DateField(blank=True, null=True)
    stud_min = models.IntegerField(blank=True, null=True)
    stud_max = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.course} is open for registration from {self.enroll_start} till {self.enroll_end}"