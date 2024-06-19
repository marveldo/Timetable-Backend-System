from django.shortcuts import render
from rest_framework import viewsets,generics,status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from .permissions import AdminTypePermission, AdminLecturerTypePermission, AdminLecturerClassrepType
from rest_framework.views import APIView
import random
from rest_framework import renderers
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


# Create your views here.

class LoginUser(TokenObtainPairView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = CustomTokenSerializer

class CreateAdmin(generics.CreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    renderer_classes = [renderers.JSONRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            self.perform_create(serializer=serializer)
            res = {
                'status': 'success',
                'data': serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        
class CreateLecturer(generics.CreateAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    renderer_classes = [renderers.JSONRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            self.perform_create(serializer=serializer)
            res = {
                'status': 'success',
                'data': serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        

class CreateStudent(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    renderer_classes = [renderers.JSONRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            self.perform_create(serializer=serializer)
            res = {
                'status': 'success',
                'data': serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        

class GetStudent(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "SpecialId"
    permission_classes = [AdminLecturerTypePermission]
    renderer_classes = [renderers.JSONRenderer]

    def put(self,request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data = request.data , partial = True)
        if serializer.is_valid(raise_exception = True):
            self.perform_update(serializer=serializer)
            res = {
                'status':"success",
                'data': serializer.data
            }
            return Response(res, status=status.HTTP_200_OK)
    
    def get(self,request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class ListLecturers(generics.ListAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    renderer_classes = [renderers.JSONRenderer]
    
class GetLecturer(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    lookup_field = "SpecialId"
    permission_classes = [AdminTypePermission]
    renderer_classes = [renderers.JSONRenderer]

    def put(self,request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data = request.data , partial = True)
       
        if serializer.is_valid(raise_exception = True):
            
            self.perform_update(serializer=serializer)
            res  = {
                'status':"success",
                'data': serializer.data
            }
            return Response(res, status=status.HTTP_200_OK)
    
    def get(self,request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class GetAdmin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    lookup_field = "SpecialId"
    permission_classes = [AdminTypePermission]
    renderer_classes = [renderers.JSONRenderer]

    def put(self,request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data = request.data , partial = True)
        if serializer.is_valid(raise_exception = True):
            self.perform_update(serializer=serializer)
            res = {
                'status':"success",
                'data': serializer.data
            }
            return Response(res, status=status.HTTP_200_OK)
    
    def get(self,request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class UpdateCurrentUser(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [renderers.JSONRenderer]
    def get_queryset(self):
        queryset = User.objects.get(SpecialId = self.request.user.SpecialId)
        return queryset
    
    def get_serializer_class(self):
        if self.request.user.user_type == "admin":
            return AdminSerializer
        if self.request.user.user_type == "lecturer":
            return LecturerSerializer
        if self.request.user.user_type == "student":
            return StudentSerializer
        
    def put(self,request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self,request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    def get(self,request,*args,**kwargs):
        return self.retrieve(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data = request.data, partial = True)
        if serializer.is_valid(raise_exception = True):
            self.perform_update(serializer=serializer)
            res = {
                "status": "success",
                'data': serializer.data
            }
            return Response(res, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        user = self.request.user 
        serializer = self.get_serializer(user,many=False)
        res = {
            "data": serializer.data
        }
        return Response(res,status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        self.perform_destroy(user)
        res ={
            'status':'success'
        }
        return Response(res, status=status.HTTP_204_NO_CONTENT)
    


class CourseViewset(viewsets.ModelViewSet):



    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes =[AdminLecturerTypePermission]
    renderer_classes = [renderers.JSONRenderer]



    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('search'):
            queryset = queryset.filter(code__icontains = self.request.GET.get('search') )
        return queryset  



class CreateAllocations(generics.CreateAPIView):
    queryset = CourseAllocation.objects.all()
    serializer_class = CourseAllocationSerializer
    permission_classes = [AdminLecturerClassrepType]
    renderer_classes = [renderers.JSONRenderer]


class ListAllocations(mixins.ListModelMixin, generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    queryset = CourseAllocation.objects.all()
    serializer_class = GetCourseAllocationSerializer
    renderer_classes = [renderers.JSONRenderer]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('search'):
            queryset = queryset.filter(level = self.request.GET.get('search'))
        return queryset
  
    def get(self,request):
        return self.list(request)
        
class EditAllocations( mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = CourseAllocation.objects.all()
    serializer_class = CourseAllocationSerializer
    permission_classes = [AdminLecturerClassrepType]
    renderer_classes = [renderers.JSONRenderer]

    def put(self,request,pk=None):
        if pk :
            return self.update(request,pk)
        else:
            return Response("No declaration for pk value", status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self,request,pk=None):
        if pk :
            return self.destroy(request,pk)
        else:
            return Response("No declaration for pk value", status=status.HTTP_400_BAD_REQUEST)
           
        
    def get(self,request,pk=None):
        if pk :
            return self.retrieve(request,pk)
        else:
             return Response("No declaration for pk value", status=status.HTTP_400_BAD_REQUEST)
            

    
class LectureRoomViewset(viewsets.ModelViewSet):
      queryset = LectureRoom.objects.all()
      permission_classes = [AdminLecturerTypePermission]
      renderer_classes = [renderers.JSONRenderer]

      serializer_class = LectureRoomSerializer


class ExamAllocationViewset(viewsets.ModelViewSet):
    permission_classes = [AdminLecturerTypePermission]
    renderer_classes = [renderers.JSONRenderer]
    queryset = ExamAllocation.objects.all()
    serializer_class = ExamAllocationsSerializer


class UpdateStudentType(generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    lookup_field = "SpecialId"
    permission_classes = [AdminLecturerTypePermission]
    renderer_classes = [renderers.JSONRenderer]

    def get(self,request,SpecialId):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many = False)
        return Response(serializer.data , status=status.HTTP_200_OK)
    def put(self,request, SpecialId):
        instance = self.get_object()
        serializer = self.get_serializer(instance , request.data, partial = True)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)





                   



        


        
        




