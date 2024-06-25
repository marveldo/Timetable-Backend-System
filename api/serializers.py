from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


USER_CHOICES  = [
    ('ADMIN', 'admin'),
    ('STUDENT', 'student'),
    ('LECTURER', 'lecturer'),
    ('CLASS_REP',"class_rep")
    
]
STUDENT_CHOICES  = [
    ('student','STUDENT'),
    ("class_rep",'CLASS_REP')
]
LEVEL = [
    ('', '---'),
    (100,"HUNDRED"),
    (200,"TWO_HUNDRED"),
    (300,"THREE_HUNDRED"),
    (400,"FOUR_HUNDRED"),
    (500,"FIVE_HUNDRED")
]

FACULTY = [
    ('', '---'),
    ("SCIENCE", "science"),
    ("ART", "art"),
    ("BUISNESS", "buisness")
]

TITLE = [
    ('', '---'),
    ("MR", "Mr"),
    ("MRS", "Mrs")
]

class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)
        if user.user_type == 'admin':
            token['first_name'] = user.first_name
            token['last_name'] = user.last_name
            token['user_type'] = user.user_type
        
        if user.user_type == 'lecturer':
            token['first_name'] = user.first_name
            token['last_name'] = user.last_name
            token['user_type'] = user.user_type
            token["Teaching_faculty"] = user.Teaching_faculty
            token["Teaching_department"] = user.Teaching_department

        if user.user_type == 'student':
            token['first_name'] = user.first_name
            token['last_name'] = user.last_name
            token['user_type'] = user.user_type
            token['level'] = user.level
            token["Faculty"] = user.Faculty
            token["department"] = user.department

        return token
    



        
class AdminSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)
    password = serializers.CharField(write_only=True, required=False)
    user_type = serializers.ChoiceField(choices=USER_CHOICES , read_only = True)
    SpecialId = serializers.CharField(required = False)
   

    class Meta :
        model = Admin
        fields = ["id","first_name","last_name", "user_type", "SpecialId", "password"]
        extra_kwargs = {'*': {'allow_blank': True}}



    def validate(self, attrs):
        if User.objects.filter(SpecialId = attrs.get('SpecialId')).exists() :
            raise serializers.ValidationError({'SpecialId': 'SpecialId already exists'})
        
        if not self.instance and not attrs.get("first_name"):
            raise serializers.ValidationError({"first_name":"First_name is needed"})
        
        if not self.instance and not attrs.get("last_name"):
            raise serializers.ValidationError({"last_name":"last_name is needed"})
        
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Password is required for creating a new user.'})
       
        
        if not self.instance and not attrs.get('SpecialId'):
            raise serializers.ValidationError({'SpecialId': 'SpecialId is required for creating a new user.'})
        return super().validate(attrs)
        
        


    def create(self, validated_data):
        user = Admin.objects.create(
            first_name = validated_data["first_name"],
            last_name = validated_data['last_name'],
            SpecialId = validated_data["SpecialId"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
    

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=False)  
        data = self.initial_data
        allowed_fields = set(self.fields.keys())
        unknown_fields = set(data.keys()) - allowed_fields  - {'csrfmiddlewaretoken'}
        allowed_fields.remove('user_type')
        if unknown_fields:
            raise serializers.ValidationError(
                f"Unknown fields found: {', '.join(unknown_fields)} allowed fields are {allowed_fields}"
            )
        return super().is_valid(raise_exception=raise_exception)
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.SpecialId = validated_data.get('SpecialId', instance.SpecialId)


        if 'password' in validated_data :
            instance.set_password(validated_data.get('password',instance.password))

        instance.save()
        return instance


class LecturerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)
    password = serializers.CharField(write_only=True, required=False)
    user_type = serializers.ChoiceField(choices=USER_CHOICES , read_only = True)
    SpecialId = serializers.CharField(required = False)
    Teaching_department = serializers.CharField(required = False)
    Teaching_faculty = serializers.ChoiceField(choices=FACULTY, required = False)
    lecturer_title = serializers.ChoiceField(choices=TITLE, required = False)
    

    class Meta :
        model = Lecturer
        fields = ["id","first_name","last_name", "user_type", "SpecialId", "password","Teaching_faculty", "Teaching_department","lecturer_phonenumber", "lecturer_title"]
        extra_kwargs = {'*': {'allow_blank': True}}




    def validate(self, attrs):
        if User.objects.filter(SpecialId = attrs.get('SpecialId')).exists() :
            raise serializers.ValidationError({'SpecialId': 'SpecialId already exists'})
        
        if not self.instance and not attrs.get("first_name"):
            raise serializers.ValidationError({"first_name":"First_name is needed"})
        
        if not self.instance and not attrs.get("last_name"):
            raise serializers.ValidationError({"last_name":"last_name is needed"})

        if not self.instance and not attrs.get('lecturer_title'):
            raise serializers.ValidationError({'lecturer_title':'lecturer_title is needed' })
        
        if not self.instance and not attrs.get('lecturer_phonenumber'):
            raise serializers.ValidationError({"lecturer_phonenumber": "PhoneNumber is needed"})
     
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Password is required for creating a new user.'})
        
        
        if not self.instance and not attrs.get('SpecialId'):
            raise serializers.ValidationError({'SpecialId': 'SpecialId is required for creating a new user.'})
        
        if not self.instance and not attrs.get('Teaching_faculty'):
            raise serializers.ValidationError({'Teaching_faculty': "Teaching_faculty is required for creating a new user"})
        
        if not self.instance and not attrs.get('Teaching_department'):
            raise serializers.ValidationError({'Teaching_department': "Teaching_department is required for creating a new user"})
        
        return  super().validate(attrs)
    
 
        
        

    def create(self, validated_data):
        user = Lecturer.objects.create(
            first_name = validated_data["first_name"],
            last_name = validated_data['last_name'],
            SpecialId = validated_data["SpecialId"],
            Teaching_faculty = validated_data["Teaching_faculty"],
            Teaching_department = validated_data["Teaching_department"] ,
            lecturer_phonenumber = validated_data["lecturer_phonenumber"],
            lecturer_title = validated_data['lecturer_title']

            )
        user.set_password(validated_data["password"])
        user.save()
        return user
    
    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=False)  
        data = self.initial_data
        allowed_fields = set(self.fields.keys())
        unknown_fields = set(data.keys()) - allowed_fields - {'csrfmiddlewaretoken'}
        allowed_fields.remove("user_type")
        if unknown_fields:
            raise serializers.ValidationError(
                f"Unknown fields found: {', '.join(unknown_fields)} allowed fields are {allowed_fields}"
            )
        return super().is_valid(raise_exception=raise_exception)
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.SpecialId = validated_data.get('SpecialId', instance.SpecialId)
        instance.Teaching_faculty = validated_data.get("Teaching_faculty", instance.Teaching_faculty)
        instance.Teaching_department = validated_data.get("Teaching_department", instance.Teaching_department)
        instance.lecturer_phonenumber = validated_data.get("lecturer_phonenumber", instance.lecturer_phonenumber)
        instance.lecturer_title = validated_data.get('lecturer_title', instance.lecturer_title)

        if 'password' in validated_data :
            instance.set_password(validated_data.get('password',instance.password))

        instance.save()
        return instance
    
class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)
    password = serializers.CharField(write_only=True, required=False)
    user_type = serializers.ChoiceField(choices=USER_CHOICES , read_only = True)
    level = serializers.ChoiceField(choices=LEVEL, required = False)
    department = serializers.CharField(required = False)
    Faculty = serializers.ChoiceField(choices=FACULTY, required = False)
    SpecialId = serializers.CharField(required = False)


    class Meta :
        model = Student
        fields = ["id","first_name","last_name", "user_type", "SpecialId","level", "password","department","Faculty"]
        extra_kwargs = {'*': {'allow_blank': True}}



    def validate(self, attrs):

        if User.objects.filter(SpecialId = attrs.get('SpecialId')).exists() :
            raise serializers.ValidationError({'SpecialId': 'SpecialId already exists'})
        
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Password is required for creating a new user.'})
    
        if not self.instance and not attrs.get('SpecialId'):
            raise serializers.ValidationError({'SpecialId': 'SpecialId is required for creating a new user.'})
          
        if not self.instance and not attrs.get("first_name"):
            raise serializers.ValidationError({"first_name":"First_name is needed"})
        
        if not self.instance and not attrs.get("last_name"):
            raise serializers.ValidationError({"last_name":"last_name is needed"})

        
        if not self.instance and not attrs.get('department'):
            raise serializers.ValidationError({'department': "department is required for creating a new user"})
        
        if not self.instance and not attrs.get('Faculty'):
            raise serializers.ValidationError({'Faculty': "Faculty is required for creating a new user"})
        
        if not self.instance and not attrs.get('level'):
            raise serializers.ValidationError({'level': "Level is required for creating a new user"})
        

        return super().validate(attrs)
        

    def create(self, validated_data):
        user = Student.objects.create(
            first_name = validated_data["first_name"],
            last_name = validated_data['last_name'],
            SpecialId = validated_data["SpecialId"],
            department = validated_data["department"],
            Faculty = validated_data["Faculty"],
            level = validated_data["level"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
    
    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=False)
        data = self.initial_data
        allowed_fields = set(self.fields.keys())
        unknown_fields = set(data.keys()) - allowed_fields - {'csrfmiddlewaretoken'}
        allowed_fields.remove("user_type")
        if unknown_fields:
            raise serializers.ValidationError(
                f"Unknown fields found: {', '.join(unknown_fields)} allowed fields are {allowed_fields}"
            )
        return super().is_valid(raise_exception=raise_exception)
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.SpecialId = validated_data.get('SpecialId', instance.SpecialId)
        instance.level = validated_data.get('level', instance.level)
        instance.department = validated_data.get('department', instance.department)
        instance.Faculty = validated_data.get('Faculty', instance.Faculty)

        if 'password' in validated_data :
            instance.set_password(validated_data.get('password',instance.password))

        instance.save()

        return instance




class CourseSerializer(serializers.ModelSerializer):

    class Meta :

        model = Course
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=False)
        data = self.initial_data
        allowed_fields = set(self.fields.keys())
        unknown_fields = set(data.keys()) - allowed_fields - {'csrfmiddlewaretoken'}
        if unknown_fields:
            raise serializers.ValidationError(
                f"Unknown fields found: {', '.join(unknown_fields)} allowed fields are {allowed_fields}"
            )
        return super().is_valid(raise_exception=raise_exception)
    
class LectureRoomSerializer(serializers.ModelSerializer):
   
    class Meta :
        model = LectureRoom
        fields = '__all__'

class GetCourseAllocationSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    lecture_room = LectureRoomSerializer()
    class Meta :

        model = CourseAllocation
        fields = '__all__'


class CourseAllocationSerializer(serializers.ModelSerializer):

    class Meta :

        model = CourseAllocation
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=False)
        data = self.initial_data
        allowed_fields = set(self.fields.keys())
        unknown_fields = set(data.keys()) - allowed_fields - {'csrfmiddlewaretoken'}
        if unknown_fields:
            raise serializers.ValidationError(
                f"Unknown fields found: {', '.join(unknown_fields)} allowed fields are {allowed_fields}"
            )
        return super().is_valid(raise_exception=raise_exception)
    



class ExamAllocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamAllocation
        fields = '__all__'


class StudentUpdateSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=STUDENT_CHOICES , required=False)
    class Meta:
        model = Student
        fields =["user_type","first_name","last_name","id"]
        extra_kwargs = {"first_name":{"read_only":True}, "last_name":{"read_only":True}}

        


    
    
    
    

        

 






    


    

        


