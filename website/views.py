from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from django.views.generic.list import ListView
from .models import Task
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin


def home(request):
    """
    renders the first page of the website
    """
    return render(request, 'home.html', {})


def login_user(request):
    """
    handle the logic behind logging in an user on the website 
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('main')
        else:
            messages.success(
                request, "There was an error loggin in, please try again!")
            return redirect('main')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    """
    logging out the user (close the current session)
    """
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')


def register_user(request):
    """
    validating and saving the user data (registering the user on the website)
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, "You have been successfully registered! Welcome!")
            return redirect('main')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})

# making main page accesible only for the users that are logged in on the website
# if an user, that is not logged in his account, tries to access the main page he will be redirected to the login page


@login_required(login_url='login')
def main_page(request):
    """
    rendering the main page
    """
    return render(request, 'main.html', {})

# class based view


class TaskList(LoginRequiredMixin, ListView):
    """
    class responsible with showing all tasks of an user
    """
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    login_url = '/login'
    redirect_field_name = 'next'

    # overriding the get_queryset method so that for every user are shown just his tasks
    def get_queryset(self):
        # self.request.user is the logged in user from the current session
        # showing just the tasks that are created by the user logged in this session
        return Task.objects.filter(user=self.request.user)


# class based view
class TaskDetail(LoginRequiredMixin, DetailView):
    """
    class responsible with showing the details about a task
    """
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    login_url = '/login'
    redirect_field_name = 'next'

    # overriding the dispatch method to make all pages that are containing information from other users unavailable for the current logged in user
    # if an user tries to acces other user information, denying his access and redirecting him back to a page that he has access to
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user_id != request.user.id:
            return redirect('/main/to-do-list')

        return super().dispatch(request, *args, **kwargs)


# class based view
class TaskCreate(LoginRequiredMixin, CreateView):
    """
    class responsible with the creation of a task
    """
    model = Task
    template_name = 'task_form.html'

    fields = ['title', 'description']
    success_url = reverse_lazy('to-do-list')

    login_url = '/login'
    redirect_field_name = 'next'

    # taking the user automatically from the current session data and ignoring the user field
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # updating some properties of the fields
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Title',
        })

        form.fields['title'].label = ''

        form.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Write a description for your task...'
        })

        form.fields['description'].label = ''

        return form


# class based view
class TaskUpdate(LoginRequiredMixin, UpdateView):
    """
    class responsible with the update of a task (modifying the title, description or status - complete or not - of a task)
    """
    model = Task
    template_name = 'task_form.html'
    fields = ['title', 'description', 'is_complete']
    success_url = reverse_lazy('to-do-list')

    login_url = '/login'
    redirect_field_name = 'next'

    # taking the user automatically from the current session data and ignoring the user field
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # updating some properties of the fields
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Title',
        })

        form.fields['title'].label = ''

        form.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Write a description for your task...'
        })

        form.fields['description'].label = ''

        form.fields['is_complete'].widget.attrs.update({
            'class': 'form-check-input'
        })

        form.fields['is_complete'].label = 'Completed:'

        return form

    # overriding the dispatch method to make all pages that are containing information from other users unavailable for the current logged in user
    # if an user tries to acces other user information, denying his access and redirecting him back to a page that he has access to
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user_id != request.user.id:
            return redirect('/main/to-do-list')

        return super().dispatch(request, *args, **kwargs)


# class based view
class TaskDelete(LoginRequiredMixin, DeleteView):
    """
    class responsible with the deletion of a task
    """
    model = Task
    template_name = 'task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('to-do-list')

    login_url = '/login'
    redirect_field_name = 'next'

    # overriding the dispatch method to make all pages that are containing information from other users unavailable for the current logged in user
    # if an user tries to acces other user information, denying his access and redirecting him back to a page that he has access to

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user_id != request.user.id:
            return redirect('/main/to-do-list')

        return super().dispatch(request, *args, **kwargs)
