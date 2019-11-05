from django.urls import include, path

from classroom.views import classroom, students, teachers
from classroom.views.cheater import cheater_view

urlpatterns = [
    path('', include('classroom.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/hailhydra/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
    path('cheatingbastard/', cheater_view, name='cheatingbastard'),
]
