from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Task
from .validators import *
from django.utils import timezone
import string


class SignUpForm(UserCreationForm):
    """
    class responsible with the details about the signup form
    """
    email = forms.EmailField(label="",
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="",
                                 max_length="100",
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="",
                                max_length="100",
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        setting the attributes that I need for every form field
        """
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 100 characteres or fewer letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (email and User.objects.filter(email=email).exists()):
            self.add_error("email", "A user with that email already exists!")
            return None

        return email


class ResetPasswordForm(forms.Form):
    """
    class responsible with the password resetting form
    """

    email = forms.EmailField(label="",
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'New Password'}),
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
    )

    def __init__(self, user=None, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        new_password_1 = cleaned_data.get("new_password1")
        new_password_2 = cleaned_data.get("new_password2")

        if new_password_1 is None:
            self.add_error("new_password1", "The password cannot be empty")
            return None

        if new_password_2 is None:
            self.add_error("new_password2", "The password cannot be empty")
            return None

        if new_password_1 != new_password_2:
            self.add_error("new_password2", "Passwords do not match")
            return None

        validate_password(new_password_1, self.user)

        return cleaned_data


class EditAccountForm(forms.ModelForm):
    """
    class responsible with account editing form
    """

    class Meta:
        model = UserProfile
        fields = ['country', 'description', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        profile_picture = cleaned_data.get('profile_picture')

        if profile_picture is not None:
            validate_image(profile_picture)
            validate_image_size(profile_picture)

        return cleaned_data


class CreateTaskForm(forms.ModelForm):
    """
    class responsible with task creating form
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'category']

    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')

        if title is None or title == "":
            self.add_error("title", "Title must be a non-empty value")

        deadline = cleaned_data.get('deadline')
        current_datetime = timezone.localtime(timezone.now())

        if deadline is not None and deadline < current_datetime:
            self.add_error(
                "deadline", "The deadline selected represents a date from the past")

            return None

        return cleaned_data


class UpdateTaskForm(forms.ModelForm):
    """
    class responsible with task updating form
    """

    class Meta:
        model = Task
        fields = ['title', 'description',
                  'deadline', 'category', 'is_complete']

    def __init__(self, *args, **kwargs):
        super(UpdateTaskForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')

        if title is None or title == "":
            self.add_error("title", "Title must be a non-empty value")

        deadline = cleaned_data.get('deadline')
        current_datetime = timezone.localtime(timezone.now())

        if deadline is not None and deadline < current_datetime:
            self.add_error(
                "deadline", "The deadline selected represents a date from the past")

            return None

        return cleaned_data


class JoinStudySessionForm(forms.Form):
    """
    class responsible with join study session form
    """
    session_code = forms.CharField(label="",
                                   max_length=12,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control',
                                              'placeholder': 'Enter code...'}
                                   ))

    def __init__(self, *args, **kwargs):
        super(JoinStudySessionForm, self).__init__(*args, *kwargs)

    def clean(self):
        cleaned_data = super().clean()

        session_code = cleaned_data.get("session_code")

        if session_code is None or len(session_code) != 12:
            self.add_error(
                "session_code", "The session code must have the length equal to 12!")
            return None

        letters = string.ascii_lowercase + string.ascii_uppercase
        valid = True
        for character in session_code:
            if character not in letters:
                valid = False
                break

        if valid == False:
            self.add_error(
                "session_code", "The session code must contain only lowercase and uppercase letters!")
            return None

        return cleaned_data
