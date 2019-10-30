"""opencurtain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from restserver.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('user/', UserDetail.as_view()),
    path('user/login/', UserLogin.as_view()),
    path('user/logout/', UserLogout.as_view()),
    path('user/post', UserPostView.as_view()),
    path('authcode/', AuthCode.as_view()),
    path('authcheck/', AuthCheck.as_view()),
    path('subscribes/', SubscribeView.as_view()),
    path('universitys/', UniversityView.as_view()),
    path('facultys/', AllFacultyView.as_view()),
    path('facultys/<int:university_id>', FacultyView.as_view()),
    path('departments/', AllDepartmentView.as_view()),
    path('departments/<int:faculty_id>', DepartmentView.as_view()),
    path('posts/<int:board_id>', PostView.as_view()),
    path('posts/', PostWriteView.as_view()),
    path('posts/<int:board_id>/<int:post_id>',APostView.as_view()),
    path('comments/<int:post_id>', CommentView.as_view()),
    path('comments/<int:post_id>/<int:comment_id>', CommentDeleteView.as_view()),
    path('media/<int:post_id>/<int:image_id>', PostWriteView.as_view()),
]
