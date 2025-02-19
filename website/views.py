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
    return render(request, 'home.html', {})


def login_user(request):
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
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')


def register_user(request):
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


@login_required(login_url='login')
def main_page(request):
    return render(request, 'main.html', {})


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    login_url = '/login'
    redirect_field_name = 'next'

    def get_queryset(self):
        # self.request.user is the logged in user from the current session
        return Task.objects.filter(user=self.request.user)


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    login_url = '/login'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user_id != request.user.id:
            return redirect('/main/to-do-list')

        return super().dispatch(request, *args, **kwargs)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task_form.html'

    fields = ['title', 'description']
    success_url = reverse_lazy('to-do-list')

    login_url = '/login'
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task_form.html'
    fields = ['title', 'description', 'is_complete']
    success_url = reverse_lazy('to-do-list')

    login_url = '/login'
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user_id != request.user.id:
            return redirect('/main/to-do-list')

        return super().dispatch(request, *args, **kwargs)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('to-do-list')

    login_url = '/login'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user_id != request.user.id:
            return redirect('/main/to-do-list')

        return super().dispatch(request, *args, **kwargs)
