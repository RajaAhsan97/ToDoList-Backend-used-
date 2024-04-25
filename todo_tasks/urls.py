from django.urls import path
from . import views

app_name = 'todoList'

urlpatterns = [
    path("", views.home, name="home-page"),
    path("list/<int:user_id>", views.ToDoListView, name="todo-list"),
    path("delete-task/<int:task_id>/<int:user_id>", views.DeleteTask, name="delete-task"),
    path("update-task/<int:task_id>/<int:user_id>", views.UpdateTask, name="update-task"),

    path("signup/", views.SignUpView, name="sign-up"),
    path("login/", views.LoginView, name="log-in"),
    path("logout/", views.LogoutView, name="log-out"),

]