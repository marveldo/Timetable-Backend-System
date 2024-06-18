from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class UserManager(BaseUserManager):

    def create(self, SpecialId, password = None , **extra_fields):

        if not SpecialId :
            raise ValueError("Matric No or Staff_id must be set")
        
        user = self.model(SpecialId = SpecialId, **extra_fields)

        user.set_password(password)

        user.save()
        return user
    
    def create_superuser(self, SpecialId, password, **extra_fields):

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin",True)
        extra_fields.setdefault("user_type", "admin")
        
        if extra_fields.get("is_active") is not True :
            raise ValueError("User Must be active")
        if extra_fields.get("is_superuser") is not True :
            raise ValueError("User Must have is_superuser = True")
        if extra_fields.get("is_staff") is not True :
            raise ValueError("User Must have is_staff = True")
        if extra_fields.get("is_admin") is not True :
            raise ValueError("User Must have is_admin = True")
        if extra_fields.get("user_type") != "admin":
            raise ValueError("User Type Must be admin")
        
        return self.create(SpecialId, password ,  **extra_fields)
    

class Level(models.TextChoices):
    HUNDRED = 100
    TWO_HUNDRED = 200
    THREE_HUNDRED = 300
    FOUR_HUNDRED = 400
    FIVE_HUNDRED = 500




class UserTypes(models.TextChoices):
    ADMIN = "admin"
    LECTURER = "lecturer"
    STUDENT = "student"
    CLASS_REP = "class_rep"

class Faculty(models.TextChoices):
    SCIENCE = "science"
    ART = "Art"
    BUISNESS = "buisness"

class Unit(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

class Day(models.TextChoices):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"

class Title(models.TextChoices):
    MR = 'Mr'
    MRS = 'Mrs'


class User(AbstractBaseUser,PermissionsMixin):

    first_name = models.CharField(max_length=120, blank = True, null = True)
    last_name = models.CharField(max_length=120, blank = True, null = True)
    lecturer_title = models.CharField(max_length=100 , blank=True, null = True , choices=models.TextChoices)
    lecturer_phonenumber = PhoneNumberField(blank = True, null = True)
    level = models.IntegerField(blank=True, null = True, choices=Level.choices)
    department = models.CharField(max_length=250, blank=True, null = True , verbose_name="student-department")
    user_type = models.CharField(max_length=120, choices=UserTypes.choices, verbose_name="type")
    Faculty = models.CharField(max_length=120, choices= Faculty.choices, blank = True , null=True ,verbose_name="students-faculty")
    Teaching_department = models.CharField(max_length=250, blank = True , null=True, verbose_name="lecturers-department")
    Teaching_faculty = models.CharField(max_length=250, choices = Faculty.choices,  blank = True , null=True, verbose_name="lecturers-faculty"    )
    SpecialId = models.CharField(max_length=250 , unique=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return str(self.SpecialId)
    
    objects = UserManager()

    USERNAME_FIELD = "SpecialId"

    REQUIRED_FIELDS = ["first_name", "last_name"]


class StudentManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(user_type = "student")

    def create(self, **kwargs):
        kwargs["user_type"] = "student"
        return super().create(**kwargs) 
    
class LecturerManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(user_type = "lecturer")
    
    def create(self, **kwargs):
        kwargs["user_type"] = "lecturer"
        return super().create(**kwargs)
    
class AdminManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(user_type = "admin")
    
    def create(self, **kwargs):
        kwargs["user_type"] = "admin"
        return super().create(**kwargs)

class Student(User):

    class Meta :
        proxy = True

    objects = StudentManager()

class Lecturer(User):
    
    class Meta :
        proxy = True
    
    objects = LecturerManager()

class Admin(User):
    
    class Meta :
        proxy = True
    
    objects = AdminManager()


class Course(models.Model):

    title = models.CharField(max_length=500 , blank = True , null = True, verbose_name="course_title")
    code = models.CharField(max_length=50, blank=True, null = True , verbose_name="course_code")
    lecturer_name = models.ForeignKey(Lecturer, blank=True , null=True ,on_delete= models.SET_NULL)
    students_number = models.IntegerField(blank = True, null = True)
    unit = models.IntegerField(null=True, blank=True, choices=Unit.choices)
    level = models.IntegerField(blank = True, null = True, choices=Level.choices)


    def __str__(self):
        return str(self.code)
    

class LectureRoom(models.Model):
    lecture_room = models.CharField(max_length=200, blank = True , null= True)


    def __str__(self):
        return str(self.lecture_room)


    
class CourseAllocation(models.Model):
    course = models.ForeignKey(Course, blank = True , null=True, on_delete=models.CASCADE)
    lecture_room = models.ForeignKey(LectureRoom, blank = True, null = True, on_delete=models.SET_NULL )
    level = models.IntegerField(blank = True, null = True, choices=Level.choices)
    start_time = models.TimeField(blank = True, null = True)
    end_time = models.TimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.course}'
    
class ExamAllocation(models.Model):
    course = models.ForeignKey(Course, blank = True , null=True, on_delete=models.CASCADE)
    lecture_room = models.ForeignKey(LectureRoom, blank = True, null = True, on_delete=models.SET_NULL )
    date = models.DateField(blank = True, null=True)
    level = models.IntegerField(blank = True, null = True, choices=Level.choices)
    start_time = models.TimeField(blank = True, null = True)
    end_tIME = models.TimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.course}'


    

     
    

    