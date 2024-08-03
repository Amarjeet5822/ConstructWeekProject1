from django.urls import path
from .views import UserLogin,UserSignup,ProjectCreate,ProjectDetail,TeamDetail,TeamListCreate,TaskCreate,TaskDetail,CommentDetail,CommentCreate



urlpatterns = [
    path('signup/',UserSignup.as_view(),name='user_signup'),
    path('login/',UserLogin.as_view(),name='user_login'),

    path('teams/',TeamListCreate.as_view(),name="team_create"),
    path('teams/<int:pk>/',TeamDetail.as_view(),name="team_update_delete"),

    path('projects/',ProjectCreate.as_view(),name='project_create'),
    path('projects/<int:pk>/',ProjectDetail.as_view(),name='project_update_delete'),

    path('tasks/',TaskCreate.as_view(),name='task_create'),
    path('tasks/<int:pk>/',TaskDetail.as_view(),name='task_update_delete'),

    path('comments/',CommentCreate.as_view(),name='comment_create'),
    path('comments/<int:pk>/',CommentDetail.as_view(),name='comment_update_delete'),
]
