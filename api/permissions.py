from rest_framework.permissions import BasePermission

class AdminTypePermission(BasePermission):

    def has_permission(self, request, view):
        
        if request.user.is_authenticated:
            return request.user.user_type == "admin"
        else:
            return False
        
class LecturerTypePermission(BasePermission):

    def has_permission(self, request, view):
        
        if request.user.is_authenticated:
            return request.user.user_type == "lecturer"
        else:
            return False
        
class AdminLecturerTypePermission(BasePermission):

    def has_permission(self, request, view):
        
        if request.user.is_authenticated :
            return request.user.user_type == "admin" or request.user.user_type == "lecturer"
        
        else : 
            return False
        
class AdminLecturerClassrepType(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated :
            return request.user.user_type == "admin" or request.user.user_type == "lecturer" or request.user.user_type == "class_rep"
        
        else :
            return False
     