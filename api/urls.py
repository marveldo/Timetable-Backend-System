from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter,APIRootView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.renderers import JSONRenderer

class CustomApiRootview(APIRootView):
    renderer_classes = [JSONRenderer]

    
class CustomRouter(DefaultRouter):
    APIRootView = CustomApiRootview
    
 


router = CustomRouter()
router.register('Courses', CourseViewset, "courseviewset")
router.register('LectureRooms',LectureRoomViewset, "lectureroomviewset")
router.register('ExamAllocations', ExamAllocationViewset, "Examallocationsviewset")

urlpatterns = [
    path('create-admin/', CreateAdmin.as_view()),
    path('create-lecturer/', CreateLecturer.as_view()),
    path('create-student/',CreateStudent.as_view()),
    path('students/<str:SpecialId>/',GetStudent.as_view()),
    path('lecturers/', ListLecturers.as_view()),
    path('lecturers/<str:SpecialId>/',GetLecturer.as_view()),
    path('admins/<str:SpecialId>/', GetAdmin.as_view()),
    path('login/', LoginUser.as_view()),
    path('change/', UpdateCurrentUser.as_view()),
    path('createallocations/', CreateAllocations.as_view()),
    path('allocations/', ListAllocations.as_view()),
    path('allocations/<str:pk>/', ListAllocations.as_view()),
    path('updatestudentype/<str:SpecialId>/', UpdateStudentType.as_view()),
    path("change-allocations/",EditAllocations.as_view()),
    path("change-allocations/<str:pk>/",EditAllocations.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

] + router.urls