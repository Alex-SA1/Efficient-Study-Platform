from django.urls import path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete
from django.conf.urls.static import static
from django.conf import settings

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
         TaskDelete.as_view(), name='delete-task'),
    path('send-verification-code/', views.send_verification_code,
         name='send_verification_code'),
    path('error-404/', views.error_404, name='error_404'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('main/my-account/', views.my_account, name='my_account')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
