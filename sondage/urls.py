"""
URL configuration for sondage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from home.views import registration, login, home_admin, home_enqueteur, create_enquete, create_enquete_enqueteur, enqueteUPD_admin, enqueteUPD_enqueteur, enqueteDelete_admin, enqueteDelete_enqueteur, view_admin, view_enqueteur, addQuestion_admin, updQuestion_adm, updQuestion_enqueteur, deleteQuestion_adm, deleteQuestion_enqueteur, addResponse_admin, addResponses_enqueteur

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', registration),
    path('login/', login, name= 'login'),
    path('home-admin/', home_admin, name='home_admin'),
    path('home-enqueteur/', home_enqueteur, name='home_enqueteur'),
    path('create-enquete/', create_enquete, name='create_enquete'),
    path('create-enquete-enqueteur/', create_enquete_enqueteur, name='create_enquete_enqueteur'),
    # Gets the enquete.id from template and puts it in pk
    # Admin urls
    path('update-enquete-admin/<str:pk>', enqueteUPD_admin, name='update_enquete_admin'),
    path('delete-enquete-admin/<str:pk>', enqueteDelete_admin, name='delete_enquete_admin'),
    path('view-enquete-admin/<str:pk>', view_admin, name='view_enquete_admin'),
    path('add-question-admin/<str:pk>', addQuestion_admin, name='add_question_admin'),
    path('update-question-admin/<str:pk>', updQuestion_adm, name='upd_question_admin'),
    path('delete-question-admin/<str:pk>', deleteQuestion_adm, name='delete_question_admin'),
    path('add-response-admin/<str:pk>', addResponse_admin, name='add_response_admin'),
    
    # Enqueteur urls
    path('update-enquete-enqueteur/<str:pk>', enqueteUPD_enqueteur, name='update_enquete_enqueteur'),
    path('delete-enquete-enqueteur/<str:pk>', enqueteDelete_enqueteur, name='delete_enquete_enqueteur'),
    path('view-enquete-enqueteur/<str:pk>', view_enqueteur, name='view_enquete_enqueteur'),
    path('add-question-enqueteur/<str:pk>', addQuestion_admin, name='add_question_enqueteur'),
    path('update-question-enqueteur/<str:pk>', updQuestion_enqueteur, name='upd_question_enqueteur'),
    path('delete-question-enqueteur/<str:pk>', deleteQuestion_enqueteur, name='delete_question_enqueteur'),
    path('add-response-enqueteur/<str:pk>', addResponses_enqueteur, name='add_response_enqueteur'),
]
