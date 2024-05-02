from django.urls import path
from todoapp import views

urlpatterns=[
    path("task/add/",views.TaskCreateView.as_view(),name="task-add"),
    path("task/all/",views.TaskListView.as_view(),name="task-list"),
    path("task/<int:pk>/",views.TaskDetailView.as_view(),name="task-detail"),
    path("task/<int:pk>/remove/",views.TaskDeleteView.as_view(),name="task-delete"),
    path("task/<int:pk>/change/",views.TaskUpdateView.as_view(),name="task-update"),
    path("register/",views.SignUpView.as_view(),name="signup"),
    path("login/",views.SignInView.as_view(),name="signin"),
    path("logout/",views.SignOutView.as_view(),name="signout")


]