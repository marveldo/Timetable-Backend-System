from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Course)
admin.site.register(CourseAllocation)
admin.site.register(ExamAllocation)