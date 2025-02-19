from django.urls import path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('main/', views.main_page, name='main'),
    path('main/to-do-list/', TaskList.as_view(), name='to-do-list'),
    path('main/to-do-list/task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('main/to-do-list/create-task/',
         TaskCreate.as_view(), name='create-task'),
    path('main/to-do-list/update-task/task/<int:pk>/',
         TaskUpdate.as_view(), name='update-task'),
    path('main/to-do-list/delete-task/task/<int:pk>/',
         TaskDelete.as_view(), name='delete-task')
]
