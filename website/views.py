from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, ResetPasswordForm, EditAccountForm
from django.views.generic.list import ListView
from .models import Task
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .utils import *
from django.core.mail import send_mail
from .decorators import login_required_restrictive
from .decorators import ajax_request_required
from django.contrib.auth.models import User
from .models import UserProfile


def home(request):
    """
    renders the first page of the website
    """
    return render(request, 'home.html', {})


def error_404(request):
    """
    method that renders a error 404 page
    """
    return render(request, 'error_404.html', {})


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


def reset_password(request):
    """
    handle the logic behind resetting a user password
    """

    if request.method == "POST":
        user_email = request.POST.get('email')

        try:
            verification_code = request.POST.get('verification_code')
            expected_verification_code_key = "reset_password:" + user_email

            check_verification_code(
                verification_code, expected_verification_code_key)

            form = ResetPasswordForm(None, request.POST)

            try:
                user = User.objects.get(email=user_email)
                form.user = user
            except User.DoesNotExist:
                form.add_error(
                    "email", "No user found with that email address")

            if user and form.is_valid():
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()

                update_session_auth_hash(request, user)

                delete_verification_code(expected_verification_code_key)

                return redirect('login')
        except Exception:
            form = ResetPasswordForm()

            messages.success(
                request, "The verification code is wrong! You must enter again all form details and request for another verification code!")

            expected_verification_code_key = "reset_password:" + user_email
            delete_verification_code(expected_verification_code_key)

            return render(request, 'reset_password.html', {'form': form})

    else:
        form = ResetPasswordForm()
        return render(request, 'reset_password.html', {'form': form})

    return render(request, 'reset_password.html', {'form': form})


@login_required_restrictive
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
        user_email = request.POST.get('email')

        try:
            verification_code = request.POST.get('verification_code')
            expected_verification_code_key = "registration:" + user_email

            check_verification_code(
                verification_code, expected_verification_code_key)

            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']

                user = authenticate(username=username, password=password)

                # other attributes will be empty at first
                UserProfile.objects.create(user=user)

                login(request, user)

                messages.success(
                    request, "You have been successfully registered! Welcome!")

                delete_verification_code(expected_verification_code_key)

                return redirect('main')

        except Exception:
            # the verification code entered by the user is wrong
            form = SignUpForm()

            messages.success(
                request, "The verification code is wrong! You must enter again all form details and request for another verification code!")

            expected_verification_code_key = "registration:" + user_email
            delete_verification_code(expected_verification_code_key)

            return render(request, 'register.html', {'form': form})

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


@ajax_request_required
def send_verification_code(request):
    """
    sending a random generated code via email to the user
    """
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')

        if request.headers.get('X-Requested-For') == 'Registration' and (not username or not email):
            return JsonResponse({'message': 'Missing fields!'}, status=400)
        elif request.headers.get('X-Requested-For') == 'Reset_Password' and not email:
            return JsonResponse({'message': 'Missing fields!'}, status=400)

        verification_code = generate_verification_code()

        record_key = ""
        if request.headers.get('X-Requested-For') == 'Registration':
            record_key = "registration:" + email

            send_mail(
                'Verification code - Registration',
                f'The verification code for {username} is: {verification_code}\nThis code will expire in 3 minutes!',
                'contdetestlucru@gmail.com',
                [f"{email}"],
            )

        else:
            # requested for password resetting
            record_key = "reset_password:" + email

            send_mail(
                'Verification code - Password Reset',
                f'The verification code is: {verification_code}\nThis code will expire in 3 minutes!',
                'contdetestlucru@gmail.com',
                [f"{email}"],
            )

        record_value = verification_code
        save_verification_code(record_key, record_value)

        return JsonResponse({'message': 'Success!'})


@login_required(login_url='login')
def my_account(request):
    """
    rendering the template for my account page
    """
    return render(request, 'my_account.html', {})


@login_required(login_url='login')
def edit_account(request):
    """
    handling request for updating the user account details
    """
    if request.method == "POST":
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        current_profile_picture = user_profile.profile_picture
        current_country = user_profile.country
        current_description = user_profile.description

        new_profile_picture = request.FILES.get('profile_picture')
        new_country = request.POST['country']
        new_description = request.POST['description']

        form = EditAccountForm(request.POST, request.FILES)

        if form.is_valid():
            if new_profile_picture is not None and current_profile_picture != new_profile_picture:
                user_profile.profile_picture.save(
                    new_profile_picture.name, new_profile_picture)

            if new_country is not None and current_country != new_country:
                setattr(user_profile, 'country', new_country)

            if new_description is not None and current_description != new_description:
                setattr(user_profile, 'description', new_description)

            user_profile.save()

            return redirect('my_account')

    else:
        form = EditAccountForm()

    return render(request, 'edit_account.html', {'form': form})
