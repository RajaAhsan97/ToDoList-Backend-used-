from django.shortcuts import render, redirect
from django.http import request
from django.contrib.auth import authenticate, login, logout
from .forms import ToDoForm, SignUpForm, LoginForm
from .models import ToDoModel, userModel

def home(request):
    return render(request, 'base.html')

def SignUpView(request):
    if request.method == "POST":
        signupForm = SignUpForm(request.POST)
        if signupForm.is_valid():
            user = signupForm.save(commit=False)
            user.set_password(signupForm.cleaned_data['password'])
            user.save()

            userModel.objects.create(username=signupForm.cleaned_data['username'], email=signupForm.cleaned_data['email'])
            return redirect('todoList:log-in')
    else:
        signupForm = SignUpForm()

    return render(request, 'authenticate/signup.html', {'form': signupForm, 'user':''})

def LoginView(request):
    if request.method == "POST":
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            cd = loginForm.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                login(request, user)

                # get loggedin user
                current_user = userModel.objects.filter(email=user.email).values_list("id", flat=True)[0]
                print(current_user)
                return redirect('todoList:todo-list', user_id=current_user)
                # return render(request, 'ToDoList.html', {'user': user})
            else:
                return render(request, 'base.html', {'error_msg': "Invalid credentials, please provide valid credentials for login"})
    else:
        loginForm = LoginForm()
    return render(request, 'authenticate/login.html', {'form': loginForm, 'user': ''})

def LogoutView(request):
    logout(request)
    return render(request, 'base.html', {'user': ''})

def ToDoListView(request, user_id):
    print("ToDoList User_id", user_id)
    user = userModel.objects.get(pk=user_id)
    all_tasks = ToDoModel.objects.filter(User=user)
    if request.method == "POST":
        task_form = ToDoForm(request.POST)
        if task_form.is_valid():
            task = task_form.cleaned_data

            tasks_count = ToDoModel.objects.filter(User=user_id).count()

            
            ToDoModel.objects.create(User=user, task=task['task'], order=tasks_count+1)

            task_form = ToDoForm()
    else:
        task_form = ToDoForm()
    
    return render(request, 'ToDoList.html', {'task_form': task_form, 'tasks': all_tasks})

def DeleteTask(request, task_id, user_id):
    print("Delete task: ", user_id)
    user = userModel.objects.get(pk=user_id)
    task_to_delete = ToDoModel.objects.get(pk=task_id)
    task_to_delete.delete()

    # reorder tasks on deleting a specific task
    tasks = ToDoModel.objects.filter(User=user)
    prev_order = 0
    tasks_count = tasks.count()
    for task in range(0, tasks_count):
        taskObj = tasks[task]
        if task == 0:
            if taskObj.order != 1:
                taskObj.order = 1
        else:
            if taskObj.order != prev_order+1:
                taskObj.order = prev_order+1
        prev_order = taskObj.order
        print("order:", taskObj.order)
        taskObj.save()

    return redirect("todoList:todo-list", user_id=user_id)

def UpdateTask(request, task_id, user_id):
    instance = ToDoModel.objects.get(pk=task_id)
    user = userModel.objects.get(pk=user_id)

    if request.method == 'POST':
        task_form = ToDoForm(request.POST)
        if task_form.is_valid():
            task = task_form.cleaned_data
            print(task['task'])
            instance.task = task['task']
            instance.save()
            all_tasks = ToDoModel.objects.filter(User = user)
            return redirect("todoList:todo-list", user_id=user_id)

    else:
        data = {
            'task': instance.task
        }
        task_form = ToDoForm(initial=data)
        all_tasks = ToDoModel.objects.filter(User=user)

    return render(request, 'update.html', {'task_form': task_form, 'tasks': all_tasks,
                                           'instance': instance.id}) 