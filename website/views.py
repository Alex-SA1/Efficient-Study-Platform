from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
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
from .decorators import login_required_restrictive, country_required
from .decorators import ajax_request_required
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.utils import timezone
from .forms import CreateTaskForm, UpdateTaskForm, JoinStudySessionForm
from django.core.cache import cache
from .serializers import StudySessionMessageSerializer


def home(request):
    """
    renders the first page of the website
    """
    return render(request, 'home.html', {})


def error_404(request):
    """
    method that renders a error 404 page
    """
    return render(request, '404.html', {})


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
            messages.error(
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

            messages.error(
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

            messages.error(
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
    tasks = Task.objects.filter(user=request.user)
    deadline_freq = {}

    for task in tasks:
        if task.deadline is not None and task.is_complete == False:
            # adjusting the deadline month to 0-indexed version of Javascript
            deadline = str(timezone.localtime(task.deadline).year) + "-" + \
                str(timezone.localtime(task.deadline).month - 1) + \
                "-" + str(timezone.localtime(task.deadline).day)

            if deadline in deadline_freq:
                deadline_freq[deadline] += 1
            else:
                deadline_freq[deadline] = 1

    currentDatetime = timezone.localtime(timezone.now()).isoformat()
    return render(request, 'main.html', {
        'datetime': currentDatetime,
        'deadlines': deadline_freq
    })


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

    paginate_by = 8

    def get(self, request, *args, **kwargs):
        url_page_specifier = 'page'
        query_dict = request.GET.copy()
        if url_page_specifier not in query_dict:
            # add default page number to url at first rendering
            # keeping all other query parameters
            query_dict[url_page_specifier] = 1
            return redirect(f"{request.path}?{query_dict.urlencode()}")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_page'] = context['page_obj']
        return context

    # overriding the get_queryset method so that for every user are shown just his tasks
    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        if 'deadline' in self.request.GET:
            deadline_date = self.request.GET.get('deadline')
            # we have to show all uncompleted tasks that have the
            # deadline date equal to the filter deadline date
            # this filter allows only pagination (no other filters are allowed; if other filters are set, the deadline filter will be ignored)
            queryset = queryset.filter(is_complete=False)
            queryset = filter_tasks_by_deadline_date(queryset, deadline_date)

            return queryset

        filter = self.request.GET.get('filter')

        if filter == "completed" or filter == "uncompleted":
            is_complete_value = True if filter == "completed" else False
            queryset = queryset.filter(is_complete=is_complete_value)
        elif filter == "deadline-over":
            current_datetime = timezone.now()
            queryset = queryset.filter(is_complete=False)
            queryset = queryset.filter(deadline__lt=current_datetime)

        return queryset

    @method_decorator(country_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

# class based view


class TaskCreate(LoginRequiredMixin, CreateView):
    """
    class responsible with the creation of a task
    """
    model = Task
    template_name = 'create_task.html'

    form_class = CreateTaskForm

    success_url = reverse_lazy('to-do-list')

    login_url = '/login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = timezone.localtime(timezone.now()).isoformat()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    @method_decorator(country_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# class based view
class TaskUpdate(LoginRequiredMixin, UpdateView):
    """
    class responsible with the update of a task (modifying the title, description or status - complete or not - of a task)
    """
    model = Task
    template_name = 'update_task.html'

    context_object_name = 'task'
    form_class = UpdateTaskForm

    success_url = reverse_lazy('to-do-list')

    login_url = '/login'
    redirect_field_name = 'next'

    # taking the user automatically from the current session data and ignoring the user field
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = timezone.localtime(timezone.now()).isoformat()
        return context

    # overriding the dispatch method to make all pages that are containing information from other users unavailable for the current logged in user
    # if an user tries to acces other user information, denying his access and redirecting him back to a page that he has access to
    @method_decorator(country_required)
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user_id != request.user.id:
            return redirect('/main/to-do-list')

        return super().dispatch(request, *args, **kwargs)


# class based view
class TaskDelete(DeleteView):
    """
    class responsible with the deletion of a task
    """
    model = Task

    context_object_name = 'task'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return JsonResponse({'message': 'Success!'})

    # overriding the dispatch method to make all pages that are containing information from other users unavailable for the current logged in user
    # if an user tries to acces other user information, denying his access and redirecting him back to a page that he has access to
    @method_decorator(require_POST)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user_id != request.user.id:
            return redirect('/main/to-do-list')

        return super().dispatch(request, *args, **kwargs)


@require_POST
@csrf_protect
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

        modified_profile_picture = False
        if new_profile_picture is not None and current_profile_picture != new_profile_picture:
            modified_profile_picture = True

        modified_country = False
        if new_country is not None and current_country != new_country:
            modified_country = True

        modified_description = False
        if new_description is not None and current_description != new_description:
            modified_description = True

        form = EditAccountForm(request.POST, request.FILES)

        if modified_profile_picture == False and modified_country == False and modified_description == False:
            form.add_error(None, "No field has been modified!")

        if form.is_valid():

            new_profile_picture = form.cleaned_data['profile_picture']

            if modified_profile_picture:
                user_profile.profile_picture.save(
                    new_profile_picture.name, new_profile_picture)

            if modified_country:
                setattr(user_profile, 'country', new_country)

            if modified_description:
                setattr(user_profile, 'description', new_description)

            user_profile.save()

            return redirect('my_account')
    else:
        form = EditAccountForm()

    return render(request, 'edit_account.html', {'form': form})


@login_required(login_url='login')
@country_required
def collaborative_study_session_menu(request):
    """
    rendering the template for collaborative study session menu page
    """

    if request.method == "POST":
        form = JoinStudySessionForm(request.POST)
        if form.is_valid():
            session_code = form.cleaned_data['session_code']

            if valid_study_session(session_code) == True:
                add_user_to_study_session(session_code, request.user.username)
                return redirect('study_session', session_code=session_code)
            else:
                messages.error(
                    request, f"There is no active study session with the following session code: {session_code}")
                return redirect('error_404')
    else:
        form = JoinStudySessionForm()

    return render(request, 'collaborative_study_session_menu.html', {'form': form})


@login_required(login_url='login')
@country_required
def study_session(request, session_code):
    """
    rendering the template for study session page
    """

    if valid_study_session(session_code) == False:
        messages.error(
            request, f"There is no active study session with the following session code: {session_code}")
        return render(request, '404.html')

    if request.method == "POST":
        remove_user_from_study_session(session_code, request.user.username)

        is_study_session_empty = study_session_empty(session_code)
        if is_study_session_empty == True:
            remove_study_session(session_code)

        return redirect('collaborative_study_session_menu')

    # fetching messages paginated
    messages_page_size = 10
    default_messages_page = 1
    current_messages_page = int(request.GET.get(
        'messages-page', default_messages_page))

    messages_page_offset = (current_messages_page - 1) * messages_page_size

    study_session_messages = StudySessionMessage.objects.filter(
        group_name=f"study_session_{session_code}").order_by("-create")

    loaded_messages = study_session_messages[messages_page_offset:
                                             messages_page_offset + messages_page_size]

    try:
        next_unloaded_message = study_session_messages[messages_page_offset +
                                                       messages_page_size]
        has_next_messages_page = True
    except IndexError:
        next_unloaded_message = None
        has_next_messages_page = False

    loaded_messages = loaded_messages[::-1]
    serialized_messages = StudySessionMessageSerializer(
        loaded_messages, many=True)

    # check if there was made an Ajax request
    # all pages except the first one are sent via Json Response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        return JsonResponse({
            'messages': serialized_messages.data,
            'has_next_messages_page': has_next_messages_page,
            'next_messages_page': current_messages_page + 1
        })

    # first messages page is sent in context data
    return render(request, 'study_session.html', {
        'session_code': session_code,
        'messages': serialized_messages.data,
        'has_next_messages_page': has_next_messages_page,
        'next_messages_page': current_messages_page + 1
    })


@require_POST
@csrf_protect
@ajax_request_required
def generate_study_session_code(request):
    """
    generate a random and unique code for a study session
    """

    if request.method == "POST":
        letters = string.ascii_lowercase + string.ascii_uppercase

        available_characters = list(letters)
        random.shuffle(available_characters)

        code_uniqueness = False
        session_code = None
        while code_uniqueness == False:
            code = ""
            for _ in range(12):
                random_index = random.randint(0, len(available_characters) - 1)
                code += available_characters[random_index]

            if valid_study_session(code) == False:
                register_study_session(code, request.user.username)
                session_code = code
                code_uniqueness = True

        return JsonResponse({'study_session_code': session_code})
