from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .views import TaskList, login_user, logout_user, register_user, main_page, home
from django.contrib.messages import get_messages


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


