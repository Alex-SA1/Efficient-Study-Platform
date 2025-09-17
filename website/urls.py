from django.urls import path
from . import views
from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete, UsersList
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('main/', views.main_page, name='main'),
    path('main/to-do-list/', TaskList.as_view(), name='to-do-list'),
    path('main/to-do-list/create-task/',
         TaskCreate.as_view(), name='create-task'),
    path('main/to-do-list/update-task/task/<int:pk>/',
         TaskUpdate.as_view(), name='update-task'),
    path('main/to-do-list/delete-task/task/<int:pk>/',
         TaskDelete.as_view(), name='delete-task'),
    path('send-verification-code/', views.send_verification_code,
         name='send_verification_code'),
    path('404/', views.error_404, name='error_404'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('main/my-account/', views.my_account, name='my_account'),
    path('main/edit-account/', views.edit_account, name='edit_account'),
    path('main/collaborative-study-session-menu/',
         views.collaborative_study_session_menu, name='collaborative_study_session_menu'),
    path('main/collaborative-study-session-menu/study-session/<str:session_code>',
         views.study_session, name='study_session'),
    path('generate-study-session-code/', views.generate_study_session_code,
         name='generate_study_session_code'),
    path('main/search_users', UsersList.as_view(), name='search_users'),
    path('send-friend-request/', views.send_friend_request,
         name="send_friend_request"),
    path('manage_friend_request/', views.manage_friend_request,
         name='manage_friend_request'),
    path('main/profile/<str:username>', views.profile, name='profile'),
    path('main/flashcards', views.flashcards, name='flashcards'),
    path('main/flashcards/create-flashcard',
         views.flashcard_create, name='create_flashcard'),
    path('main/flashcards/folder/<str:folder_name>', views.folder, name='folder'),
    path('main/flashcards/update-flashcard/flashcard/<int:pk>',
         views.flashcard_update, name='update_flashcard'),
    path('main/flashcards/delete-flashcard/flashcard/<int:pk>',
         views.flashcard_delete, name='delete_flashcard'),
    path('main/flashcards/delete-folder/folder/<int:pk>',
         views.folder_delete, name='delete_folder')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
