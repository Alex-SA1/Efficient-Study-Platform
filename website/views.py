from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import SignUpForm, ResetPasswordForm, EditAccountForm, FlashcardsFolderForm, FlashcardForm
from django.views.generic.list import ListView
from .models import Task, UserProfile, FriendRequest, Friendship, FlashcardsFolder, Flashcard
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
from django.core.exceptions import ValidationError
from django.utils import timezone
from .forms import CreateTaskForm, UpdateTaskForm, JoinStudySessionForm
from django.core.cache import cache
from .serializers import StudySessionMessageSerializer
import re
from django.core.paginator import Paginator


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
        query_dict = request.GET.copy()
        query_dict_modified = False

        url_filter_specifier = 'filter'
        url_deadline_specifier = 'deadline'
        if url_filter_specifier not in query_dict and url_deadline_specifier not in query_dict:
            # set the default filter to "all" when no filter is set
            query_dict[url_filter_specifier] = 'all'
            query_dict_modified = True

        url_page_specifier = 'page'
        if url_page_specifier not in query_dict:
            # add default page number to url at first rendering
            # keeping all other query parameters
            query_dict[url_page_specifier] = 1
            query_dict_modified = True

        if query_dict_modified == True:
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
        try:
            task = self.get_object()
        except:
            return JsonResponse({
                'error': "The task that you are trying to delete either doesn't exists or you have no access to it!"
            }, status=400)

        if task.user_id != request.user.id:
            return JsonResponse({
                'error': "The task that you are trying to delete either doesn't exists or you have no access to it!"
            }, status=400)

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
    query_dict = request.GET.copy()
    url_page_specifier = 'page'
    url_action_specifier = 'action'

    if url_action_specifier in query_dict and url_page_specifier not in query_dict:
        query_dict['page'] = 1
        return redirect(f"{request.path}?{query_dict.urlencode()}")

    if url_action_specifier in query_dict:
        action = request.GET.get('action')
        if action == "friend-requests-inbox":
            friend_requests = FriendRequest.objects.filter(
                receiver=request.user, status='pending')
            paginator = Paginator(friend_requests, 20)

            page_number = query_dict.get('page')
            friend_requests_page = paginator.get_page(page_number)

            return render(request, 'my_account.html', {
                'friend_requests_inbox': True,
                'friend_requests_page': friend_requests_page
            })

    return render(request, 'my_account.html', {
        'friend_requests_inbox': False
    })


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
        if new_country is not None and current_country != new_country and new_country != "Select country":
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


class UsersList(LoginRequiredMixin, ListView):
    """
    class responsible with showing users according to an entered keyword
    """
    model = User
    template_name = 'search_users.html'
    context_object_name = 'users'

    login_url = '/login'
    redirect_field_name = 'next'

    paginate_by = 20

    def get(self, request, *args, **kwargs):
        query_dict = request.GET

        url_search_string_specifier = 'username'
        if url_search_string_specifier in query_dict:
            search_string = query_dict[url_search_string_specifier]
            if search_string == "":
                return redirect(request.path)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = User.objects.none()

        if 'username' in self.request.GET:
            input_username = self.request.GET.get('username')

            username_regex = r"^[\w.@+-]{1,150}\Z"
            if re.match(username_regex, input_username):
                queryset = User.objects.filter(
                    username__startswith=input_username)

        return queryset


@require_POST
@csrf_protect
@ajax_request_required
def send_friend_request(request):
    """
    send a friend request to a user
    """

    if request.method == "POST":
        data = json.loads(request.body)
        receiver_username = data.get('receiver_username')
        sender_user = request.user

        if sender_user.username == receiver_username:
            return JsonResponse({
                'error': "You can't send a friend request to yourself!",
            }, status=400)

        try:
            receiver_user = User.objects.get(username=receiver_username)
        except:
            return JsonResponse({
                'error': "The receiver username doesn't correspond to an user!"
            }, status=400)

        friend_request = get_friend_request(sender_user, receiver_user)

        if friend_request is not None:
            status = friend_request.status

            if status == "pending":
                if friend_request.sender.username == sender_user.username:
                    return JsonResponse({
                        'error': "You already sent a friend request to this user!"
                    }, status=400)
                else:
                    return JsonResponse({
                        'error': "There is a pending friend request sent by this user to you!"
                    }, status=400)
            elif status == "accepted":
                return JsonResponse({
                    'error': "You are friend with this user!"
                }, status=400)
            elif status == "rejected":
                # change the status of the friend request from "rejected" to "pending"
                setattr(friend_request, 'status', 'pending')
                if friend_request.sender.username != sender_user.username:
                    setattr(friend_request, 'receiver', friend_request.sender)
                    setattr(friend_request, 'sender', sender_user)

                friend_request.save()

            return JsonResponse({
                'message': 'Success!'
            })

        FriendRequest.objects.create(
            sender=sender_user, receiver=receiver_user)

        return JsonResponse({
            'message': 'Success!'
        })


@require_POST
@csrf_protect
@ajax_request_required
def manage_friend_request(request):
    """
    accept/reject a friend request
    """

    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get('action')
        sender_username = data.get('sender_username')
        receiver_user = request.user

        try:
            sender_user = User.objects.get(username=sender_username)
        except:
            return JsonResponse({
                'error': "The sender username doesn't correspond to an user!"
            }, status=400)

        friend_request = get_friend_request(sender_user, receiver_user)

        if friend_request is None:
            return JsonResponse({
                'error': f"There is no friend request sent by {sender_username} to you!"
            }, status=400)

        if action == "accept":
            setattr(friend_request, 'status', 'accepted')
            friend_request.save()

            Friendship.objects.create(
                user_1=sender_user,
                user_2=receiver_user
            )
        elif action == "reject":
            setattr(friend_request, 'status', 'rejected')
            friend_request.save()

        return JsonResponse({
            'message': 'Success!'
        })


@login_required(login_url='login')
def profile(request, username):
    """
    renders a page for user profile
    """
    try:
        user = User.objects.get(username=username)
    except:
        return render(request, '404.html')

    return render(request, 'profile.html', {
        'profile_user': user
    })


@login_required(login_url='login')
def flashcards(request):
    """
    renders the main page for the flashcards app
    """
    if request.method == "POST":
        form_type = None
        if ('create_folder_form' in request.POST and request.POST.get('create_folder_form') == 'CreateFolderForm' and
                'create_folder_btn' in request.POST and request.POST.get('create_folder_btn') == 'Create'):
            form_type = 'Create'
        elif ('update_folder_form' in request.POST and request.POST.get('update_folder_form') == 'UpdateFolderForm' and
              'update_folder_btn' in request.POST and request.POST.get('update_folder_btn') == 'Update'):
            form_type = 'Update'

        if form_type is None:
            messages.error(request, "The folder submitted is invalid!")
            form = FlashcardsFolderForm()
            create_folder_form = form
            update_folder_form = form
        else:
            error = False
            if form_type == 'Update':
                folder_id = request.POST.get('folder_id')
                try:
                    folder = FlashcardsFolder.objects.get(
                        user=request.user, pk=folder_id)
                    update_folder_form = FlashcardsFolderForm(
                        request.user, form_type, folder, request.POST)
                except:
                    folder = None
                    error = True
                    messages.error(
                        request, "The folder that you are trying to update either doesn't exists or you have no access to it!")
                    update_folder_form = FlashcardsFolderForm()

                create_folder_form = FlashcardsFolderForm()
            elif form_type == 'Create':
                create_folder_form = FlashcardsFolderForm(
                    request.user, form_type, None, request.POST)
                update_folder_form = FlashcardsFolderForm()

            if error == False and form_type == 'Create' and create_folder_form.is_valid():
                folder_name = create_folder_form.cleaned_data['name']

                FlashcardsFolder.objects.create(
                    user=request.user, name=folder_name)

                return redirect('flashcards')
            elif error == False and form_type == 'Update' and update_folder_form.is_valid():
                folder_name = update_folder_form.cleaned_data['name']

                setattr(folder, 'name', folder_name)
                folder.save()

                return redirect('flashcards')
            else:
                messages.error(
                    request, f"The form has some errors! Open the form to see the errors!")
    else:
        form = FlashcardsFolderForm()
        create_folder_form = form
        update_folder_form = form

    folders = FlashcardsFolder.objects.filter(user=request.user)

    return render(request, 'flashcards.html', {
        'create_folder_form': create_folder_form,
        'update_folder_form': update_folder_form,
        'folders': folders
    })


@login_required(login_url='login')
def flashcard_create(request):
    """
    renders and handles the flashcard creation form
    """

    if request.method == "POST":
        form = FlashcardForm(request.user, request.POST)

        if form.is_valid():
            folder = form.cleaned_data['folder']
            front_side_text = form.cleaned_data['front_side_text']
            back_side_text = form.cleaned_data['back_side_text']

            Flashcard.objects.create(user=request.user, folder=folder,
                                     front_side_text=front_side_text, back_side_text=back_side_text)

            increment_folder_flashcards_number(folder)

            return redirect('flashcards')
    else:
        form = FlashcardForm()

    flashcards_folders = FlashcardsFolder.objects.filter(user=request.user)
    folder_names = [folder.name for folder in flashcards_folders]

    return render(request, 'create_flashcard.html', {
        'folder_names': folder_names,
        'form': form
    })


@login_required(login_url='login')
def flashcard_update(request, pk):
    """
    renders and handles the flashcard update form
    """
    try:
        flashcard = Flashcard.objects.get(pk=pk, user=request.user)
    except:
        return render(request, '404.html', {})

    if request.method == "POST":
        form = FlashcardForm(request.user, request.POST)

        if form.is_valid():
            new_folder = form.cleaned_data['folder']
            new_front_side_text = form.cleaned_data['front_side_text']
            new_back_side_text = form.cleaned_data['back_side_text']

            folder_modified = False
            if new_folder.name != flashcard.folder.name:
                folder_modified = True
                decrement_folder_flashcards_number(flashcard.folder)

                new_folder = FlashcardsFolder.objects.get(
                    user=request.user, name=new_folder.name)
                increment_folder_flashcards_number(new_folder)

                setattr(flashcard, "folder", new_folder)

            front_side_text_modified = False
            if new_front_side_text != flashcard.front_side_text:
                print(new_front_side_text, flashcard.front_side_text)
                front_side_text_modified = True
                setattr(flashcard, "front_side_text", new_front_side_text)

            back_side_text_modified = False
            if new_back_side_text != flashcard.back_side_text:
                print(new_back_side_text, flashcard.back_side_text)
                back_side_text_modified = True
                setattr(flashcard, "back_side_text", new_back_side_text)

            if folder_modified or front_side_text_modified or back_side_text_modified:
                flashcard.save()
                return redirect('flashcards')

            form.add_error(None, "No field has been modified")
    else:
        form = FlashcardForm()

    flashcards_folders = FlashcardsFolder.objects.filter(user=request.user)
    folder_names = [folder.name for folder in flashcards_folders]

    return render(request, 'update_flashcard.html', {
        'flashcard': flashcard,
        'folder_names': folder_names,
        'form': form
    })


@require_POST
@csrf_protect
def flashcard_delete(request, pk):
    """
    handles the flashcard delete request
    """
    try:
        flashcard = Flashcard.objects.get(pk=pk, user=request.user)
    except:
        return JsonResponse({
            'error': "The flashcard that you are trying to delete either doesn't exists or you have no access to it!"
        }, status=400)

    if request.method == "POST":
        flashcard_folder = flashcard.folder
        flashcard.delete()
        decrement_folder_flashcards_number(flashcard_folder)

        return JsonResponse({'message': 'Success!'})


@login_required(login_url='login')
def folder(request, folder_name):
    """
    renders a flashcards folder page
    """

    try:
        folder = FlashcardsFolder.objects.get(
            user=request.user, name=folder_name)
    except:
        messages.error(
            request, "The folder that you are trying to access either doesn't exists or belongs to another user!")
        return render(request, '404.html')

    flashcards = Flashcard.objects.filter(user=request.user, folder=folder)

    return render(request, 'folder.html', {
        'folder_name': folder_name,
        'flashcards': flashcards
    })


@require_POST
@csrf_protect
def folder_delete(request, pk):
    """
    handles the folder delete request
    """

    try:
        folder = FlashcardsFolder.objects.get(user=request.user, pk=pk)
    except:
        return JsonResponse({
            'error': "The folder that you are trying to delete either doesn't exists or you have no access to it!"
        }, status=400)

    if request.method == "POST":
        folder.delete()

        return JsonResponse({'message': 'Success!'})
