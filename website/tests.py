from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .views import TaskList, login_user, logout_user, register_user, main_page, home, TaskDetail, TaskCreate, TaskUpdate, TaskDelete
from django.contrib.messages import get_messages
from .models import Task
from django.contrib.auth.models import AnonymousUser


class TestHomePage(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse(home))

        # the status code for rendering with success a page is 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class TestUserLogin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', password='passwd123')

    def test_login_page_loads(self):
        response = self.client.get(reverse(login_user))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_success(self):
        response = self.client.post(reverse(login_user),
                                    {'username': 'test', 'password': 'passwd123'})

        self.assertRedirects(response, reverse('main'))

        self.assertIsNotNone(self.user)
        self.assertTrue(self.user.is_authenticated)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You have been logged in!")

    def test_login_fail(self):
        response = self.client.post(reverse(login_user),
                                    {'username': 'test', 'password': 'newpasswd'})

        user = self.client.session.get('_auth_user_id')
        self.assertIsNone(user)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         "There was an error loggin in, please try again!")

    def tearDown(self):
        self.client.logout()


class TestUserLogout(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password='passwd123')
        self.client.login(username='user', password='passwd123')

    def test_logout(self):
        response = self.client.post(reverse(logout_user),
                                    {'username': 'user', 'password': 'passwd123'})

        user = self.client.session.get('_auth_user_id')
        self.assertIsNone(user)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You have been logged out!")

        self.assertRedirects(response, reverse('home'))


class TestUserRegister(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse(register_user))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_success(self):
        response = self.client.post(reverse(register_user),
                                    {'username': 'new_user',
                                     'email': 'user_email@gmail.com',
                                     'first_name': 'user_first_name',
                                     'last_name': 'user_last_name',
                                     'password1': 'user_password',
                                     'password2': 'user_password'})

        self.assertTrue(User.objects.filter(username='new_user').exists())
        self.assertEqual(User.objects.get(
            username='new_user').email, 'user_email@gmail.com')

        self.assertRedirects(response, reverse('main'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "You have been successfully registered! Welcome!")

        user = self.client.session.get('_auth_user_id')
        self.assertIsNotNone(user)

    def test_register_fail(self):
        # testing some cases in which the registration of the user fails

        response = self.client.post(reverse(register_user),
                                    {'username': 'new_user',
                                     'email': 'user_email@gmail.com',
                                     'first_name': 'user_first_name',
                                     'last_name': 'user_last_name',
                                     'password1': 'user_password',
                                     'password2': 'just_password'})

        # the passwords are different so the user can't be created
        self.assertFalse(User.objects.filter(username='new_user').exists())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(reverse(register_user),
                                    {'username': '&new_user*',
                                     'email': 'user_email@gmail.com',
                                     'first_name': 'user_first_name',
                                     'last_name': 'user_last_name',
                                     'password1': 'user_password',
                                     'password2': 'user_password'})

        # invalid characters in the username so the user can't be created
        self.assertFalse(User.objects.filter(username='&new_user*').exists())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(reverse(register_user),
                                    {'username': 'new_user',
                                     'email': 'user_email@gmail.com',
                                     'first_name': 'user_first_name',
                                     'last_name': 'user_last_name',
                                     'password1': 'pas',
                                     'password2': 'pas'})

        # password has less than 8 characters so the account can't be created
        self.assertFalse(User.objects.filter(username='new_user').exists())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(reverse(register_user),
                                    {'username': 'new_user',
                                     'email': 'user_email@gmail.com',
                                     'first_name': 'user_first_name',
                                     'last_name': 'user_last_name',
                                     'password1': 'user_first_name1',
                                     'password2': 'user_first_name_1'})

        # password is too similar with other personal information so the account can't be created
        self.assertFalse(User.objects.filter(username='new_user').exists())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(reverse(register_user),
                                    {'username': 'new_user',
                                     'email': 'user_email@gmail.com',
                                     'first_name': 'user_first_name',
                                     'last_name': 'user_last_name',
                                     'password1': '1234567890',
                                     'password2': '1234567890'})

        # password is entirely numeric so the account can't be created
        self.assertFalse(User.objects.filter(username='new_user').exists())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')


class TestMainPage(TestCase):
    def test_main_page_loads(self):
        # logging in an user and testing if the page is rendering properly
        self.user = User.objects.create_user(
            username='test', password='testpasswd123')
        self.client.login(username='test', password='testpasswd123')

        response = self.client.get(reverse(main_page))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_login_required_main_page(self):
        self.user = User.objects.create_user(
            username='User', password='passwd123paswd')

        user = self.client.session.get('_auth_user_id')
        self.assertIsNone(user)  # if user is None => user is not logged in

        # when trying to acces main page without being logged in
        # the acces should be denied and user redirected to login page
        # with next redirect page (if he loggs in) being main page

        response = self.client.get(reverse(main_page))

        # the http 302 status code indicates that the requested
        # resource has been temporarily moved to a different URL
        # and the client has been redirected to another URL

        # we should receive 302 status code for the request
        # because user is not logged in and he will be redirected
        # to login page (the access to main page is denied) with
        # next redirect address (if he loggs in) being main page
        self.assertEqual(response.status_code, 302)

        # check if he is redirected to login page with the main as next url
        self.assertRedirects(response, reverse('login') + '?next=/main/')


class TestTaskList(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('to-do-list'))
        self.view = TaskList()
        self.view.setup(self.request)

    def tearDown(self):
        self.client.logout()

    def test_task_list_page_loads(self):
        # the page is accessible only if the user is logged in
        # I'll log in an user to test if the page is rendering properly

        self.request.user = User.objects.create_user(
            username='user', password='passwd123test')
        self.client.login(username='user', password='passwd123test')

        response = TaskList.as_view()(self.request)

        self.assertEqual(response.status_code, 200)

        # response.template_name will return a list with the fallback template page and the default template page
        self.assertIn('task_list.html', response.template_name)

    def test_login_required_task_list_page(self):
        # the page is inaccessible for a user that is not logged in
        # if a logged out user tries to acces the page he will be
        # redirected to the login page

        self.request.user = AnonymousUser()
        response = TaskList.as_view()(self.request)

        self.assertEqual(response.status_code, 302)
        # 'Location' is a response header that indicates the URL
        # to redirect a page to
        # the 'Location' response header has a meaning only in
        # cases of redirection responses
        self.assertEqual(response.headers.get('Location'),
                         '/login?next=/main/to-do-list/')

    def test_get_queryset_override(self):
        self.user_1 = User.objects.create(
            username='user_1',
            password='passwd123'
        )

        self.user_2 = User.objects.create(
            username='user_2',
            password='passwd12345'
        )

        self.task_1 = Task.objects.create(
            user=self.user_1,
            title='Task_1',
            description='Standard description for task 1',
            is_complete=0
        )

        self.task_2 = Task.objects.create(
            user=self.user_1,
            title='Task_2',
            description='Standard description of task 2',
            is_complete=1
        )

        self.task_3 = Task.objects.create(
            user=self.user_2,
            title='Task_3',
            description='Standard description for task 3',
            is_complete=0
        )

        self.request.user = self.user_1
        self.client.login(username='user_1', password='passwd123')

        tasks = self.view.get_queryset()
        self.assertIn(self.task_1, tasks)
        self.assertIn(self.task_2, tasks)
        self.assertNotIn(self.task_3, tasks)


class TestTaskDetail(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password='passwd123')

        self.task = Task.objects.create(
            user=self.user,
            title='Task',
            description='Standard description for task',
            is_complete=0
        )

        self.request = RequestFactory().get(
            reverse('task', kwargs={'pk': self.task.pk}))
        self.view = TaskDetail()
        self.view.setup(self.request)

    def tearDown(self):
        self.client.logout()

    def test_task_detail_page_loads(self):
        self.request.user = self.user

        self.client.login(username='user', password='passwd123')

        response = TaskDetail.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIn('task_detail.html', response.template_name)

    def test_login_required_task_detail_page(self):
        self.anonymous_user = AnonymousUser()

        self.request.user = self.anonymous_user

        response = TaskDetail.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'),
                         '/main/to-do-list')

        # when user tries to access a task and he is not logged in
        # the LoginRequiredMixin method will redirect him to
        # the page will all his tasks and after that will check
        # again if the user is logged in (because to access the page with all his
        # tasks he needs to be logged in) and if not he will be redirected
        # to the login page

        # but we send just a request to the website while testing
        # the login required for viewing a task so the redirected
        # url will be the page will all tasks
        # so we have to make another request to the website with the
        # redirected link to check if the LoginRequiredMixin method
        # denies the user acces and redirects him to login page
        # and asking him to login to acces the previous pages

        # the idea is that when we do the second request to the website
        # with the redirected url (redirected url will be an url to to-do-list
        # page throw by a method from the TaskDetail class) we have
        # to make it with a class based view that renders the tasks list (TaskList)

        redirected_url = response.headers.get('Location')
        self.request = RequestFactory().get(redirected_url)
        self.request.user = self.anonymous_user

        response = TaskList.as_view()(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'),
                         '/login?next=/main/to-do-list')

        # so after all this process of trying to access pages with login
        # required, the user will be, finally, redirected to the login page

    def test_user_registrations_privacy(self):

        # testing if a user has access only to the registrations made
        # by him

        # if a logged in user tries to access details page for a registration
        # made by another user he will be redirected to the page with all
        # his tasks (the access to the registration from another user will be denied)

        self.user_1 = User.objects.create_user(
            username='user_1', password='parola123')

        self.task_1 = Task.objects.create(
            user=self.user_1,
            title='Task',
            description='Standard description for task',
            is_complete=0
        )

        # we will trying to access (from the perspective of the current logged in user)
        # the task of the user_1 (the access should be denied)

        self.request = RequestFactory().get(
            reverse('task', kwargs={'pk': self.task_1.pk}))

        self.request.user = self.user
        self.client.login(username='user', password='passwd123')

        response = TaskDetail.as_view()(self.request, pk=self.task_1.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'), '/main/to-do-list')

        self.client.logout()

        # now we are making a request (from the perspective of the current logged in user)
        # to one of his tasks (the acces should be granted)

        self.request = RequestFactory().get(
            reverse('task', kwargs={'pk': self.task.pk}))

        self.request.user = self.user
        self.client.login(username='user', password='passwd123')

        response = TaskDetail.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIn('task_detail.html', response.template_name)


class TestTaskCreate(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password='passwd123')

        self.request = RequestFactory().get(reverse('create-task'))
        self.view = TaskCreate()
        self.view.setup(self.request)

    def tearDown(self):
        self.client.logout()

    def test_create_task_page_loads(self):
        self.request.user = self.user
        self.client.login(username='user', password='passwd123')

        response = TaskCreate.as_view()(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('task_form.html', response.template_name)

    def test_login_required_create_task_page(self):
        self.request.user = AnonymousUser()

        response = TaskCreate.as_view()(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'),
                         '/login?next=/main/to-do-list/create-task/')

    def test_create_task_success(self):
        self.request = RequestFactory().post(reverse('create-task'), {
            'title': 'Task',
            'description': 'a short description of the task',
            'is_complete': 0
        })

        self.request.user = self.user

        response = TaskCreate.as_view()(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'), '/main/to-do-list/')

        task_object = Task.objects.filter(title='Task')

        self.assertIsNotNone(task_object)

        self.assertEqual(task_object.get().user, self.user)
        self.assertEqual(task_object.get().title, 'Task')
        self.assertEqual(task_object.get().description,
                         'a short description of the task')
        self.assertEqual(task_object.get().is_complete, 0)


class TestTaskUpdate(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password='passwd123')

        self.task = Task.objects.create(
            user=self.user,
            title='Task',
            description='Standard description for task',
            is_complete=0
        )

        self.request = RequestFactory().get(
            reverse('update-task', kwargs={'pk': self.task.pk}))
        self.view = TaskUpdate()
        self.view.setup(self.request)

    def tearDown(self):
        self.client.logout()

    def test_update_task_page_loads(self):
        self.request.user = self.user

        self.client.login(username='user', password='passwd123')

        response = TaskUpdate.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIn('task_form.html', response.template_name)

    def test_login_required_update_task_page(self):
        self.anonymous_user = AnonymousUser()
        self.request.user = self.anonymous_user

        response = TaskUpdate.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'), '/main/to-do-list')

        redirected_url = response.headers.get('Location')

        self.request = RequestFactory().get(redirected_url)
        self.request.user = self.anonymous_user

        response = TaskList.as_view()(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'),
                         '/login?next=/main/to-do-list')

    def test_user_registrations_privacy(self):
        # testing if an user can update only his tasks
        # and if he tries to access the update task page of the task
        # from another user his access will be denied and he will
        # be redirected to aa page that he has access to

        self.user_1 = User.objects.create_user(
            username='user_1', password='passwd123new')
        self.task_1 = Task.objects.create(
            user=self.user_1,
            title='Task 1',
            description='A short description of the task',
            is_complete=0
        )

        self.request = RequestFactory().get(
            reverse('update-task', kwargs={'pk': self.task_1.pk}))
        self.request.user = self.user
        self.client.login(username='user', password='passwd123')

        response = TaskUpdate.as_view()(self.request, pk=self.task_1.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'), '/main/to-do-list')

        self.client.logout()

        self.request = RequestFactory().get(
            reverse('update-task', kwargs={'pk': self.task.pk}))
        self.request.user = self.user

        response = TaskUpdate.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIn('task_form.html', response.template_name)

    def test_update_task_details(self):
        self.request.user = self.user
        self.client.login(username='user', password='passwd123')

        response = TaskUpdate.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 200)

        task_object = Task.objects.filter(pk=self.task.pk)

        self.assertEqual(task_object.get().user, self.user)
        self.assertEqual(task_object.get().title, 'Task')
        self.assertEqual(task_object.get().description,
                         'Standard description for task')
        self.assertEqual(task_object.get().is_complete, 0)

        self.request = RequestFactory().post(reverse('update-task', kwargs={'pk': self.task.pk}), {
            'title': 'New task title',
            'description': 'modified description',
            'is_complete': 1
        })

        self.request.user = self.user
        self.client.login(username='user', password='passwd123')

        response = TaskUpdate.as_view()(self.request, pk=self.task.pk)

        task_object = Task.objects.filter(pk=self.task.pk)

        self.assertIsNotNone(task_object)

        self.assertEqual(task_object.get().user, self.user)
        self.assertEqual(task_object.get().title, 'New task title')
        self.assertEqual(task_object.get().description, 'modified description')
        self.assertEqual(task_object.get().is_complete, 1)


class TestTaskDelete(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password='passwd123')

        self.task = Task.objects.create(
            user=self.user,
            title='Task',
            description='Standard description for task',
            is_complete=0
        )

        self.request = RequestFactory().get(
            reverse('delete-task', kwargs={'pk': self.task.pk}))
        self.view = TaskDelete()
        self.view.setup(self.request)

    def tearDown(self):
        self.client.logout()

    def test_delete_task_page_loads(self):
        self.request.user = self.user
        self.client.login(username='user', password='passwd123')

        response = TaskDelete.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIn('task_confirm_delete.html', response.template_name)

    def test_login_required_delete_task_page(self):
        self.anonymous_user = AnonymousUser()
        self.request.user = self.anonymous_user

        response = TaskDelete.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'), '/main/to-do-list')

        redirected_url = response.headers.get('Location')
        self.request = RequestFactory().get(redirected_url)
        self.request.user = self.anonymous_user

        response = TaskList.as_view()(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'),
                         '/login?next=/main/to-do-list')

    def test_user_registrations_privacy(self):
        # testing if an user can delete only his tasks
        # and if he tries to acces the deletion page of a task from
        # another user his access will be denied and he will be
        # redirected to another page

        self.user_1 = User.objects.create_user(
            username='user_1', password='passwd123new')
        self.task_1 = Task.objects.create(
            user=self.user_1,
            title='Task 1',
            description='A short description of the task',
            is_complete=0
        )

        self.request = RequestFactory().get(
            reverse('delete-task', kwargs={'pk': self.task_1.pk}))
        self.request.user = self.user
        self.client.login(username='user', password='passwd123')

        response = TaskDelete.as_view()(self.request, pk=self.task_1.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'), '/main/to-do-list')

        self.client.logout()

        self.request = RequestFactory().get(
            reverse('delete-task', kwargs={'pk': self.task.pk}))
        self.request.user = self.user

        response = TaskDelete.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIn('task_confirm_delete.html', response.template_name)

    def test_delete_task(self):
        self.request.user = self.user
        self.client.login(username='user', password='passwd123')

        response = TaskDelete.as_view()(self.request, pk=self.task.pk)

        self.assertTrue(response.status_code, 200)
        self.assertIn('task_confirm_delete.html', response.template_name)

        self.assertIsNotNone(Task.objects)
        self.assertEqual(Task.objects.count(), 1)

        self.request = RequestFactory().post(
            reverse('delete-task', kwargs={'pk': self.task.pk}))
        self.request.user = self.user

        response = TaskDelete.as_view()(self.request, pk=self.task.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'), '/main/to-do-list/')

        task_objects = list(Task.objects.all())
        self.assertListEqual(task_objects, [])
        self.assertEqual(Task.objects.count(), 0)
