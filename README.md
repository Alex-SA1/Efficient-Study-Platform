#* I am still working on readme file...*
# Efficient Study Platform

> *Motivation: I built this project because I wanted to learn a new web framework (Django)  and different kinds of tools and techniques related to full stack development. I chose the project topic guided by the wish of creating something that has a real life applicability and also that would help me.*

------------

### Description
The purpose of the application is to provide an online environment for students that will help them in the study process.

Navigating through the app you will find a tasks management system, a place for creating flashcards, the possibility of editing your own user profile and sending friend requests and also, a section where you can connect with your friends and start live chatting. If you are the kind of person that likes to study for fixed and organised periods of time, the pomodoro timer that you will find in the study session section may help you.

### Project features
- Registration with mail confirmation (username and email are unique fields)
- Forgot password option
- User profile section that allows the user to set a profile picture, a country or a profile description
- Search for users
- Friend requesting
- Create/update/delete tasks
- Filter tasks based on status (completed/uncompleted/deadline over)
- Calendar which contains days colored differently based on the number of tasks with the deadline set to that day
- View the tasks with the deadline set to a certain day
- View tasks paginated
- Create/update/delete flashcards
- Create/update/delete folders for flashcards
- Use pomodoro timer (edit default number of minutes)
- Live chat with friends in a dedicated section (where a user has access only if he is friend with at least one of the participating members)
- Datetime based on the user timezone
- Access restricted for users without a country selected
- No access to the application features for anonymous users (visitors without an account)


### Project Presentation

------------

#### Home Page
![home-page](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/home_page.png?raw=true)

On this page you will find just some presentation text and two buttons for accessing the login and registration pages.


------------

#### Registration Page
![registration-page](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/register_page.png?raw=true)

Here you will find a registration form with the following field constraints (if the form is submitted with invalid data, you will be notified about it and the account won't be created):
-  Username: should be unique
-  Email: should be unique and valid
- Verification Code: should be equal with the one received on email
- Password: minimum 8 characters, not too similar to username and email, not a common password, not entirely numeric

This is how the verification mail sent to you would look like.
![registration-code](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/regsitration_code.png?raw=true)

Note: The email will be marked as spam because is sent from a testing email address and not from an oficial domain.

Below you will find an image with the registration form filled with data. The password is shown because I clicked on the eye icon.

![registration-form-filled](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/registration_form_filled.png?raw=true)

------------

#### Login Page
![login-page](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/login_page.png?raw=true)

On the login page you will be asked for your account username and password. You can click on eye icon and the password will be revelead for a few seconds. Also, you will find useful links on this page such as a redirection link to the "Forgot Password" page or to the registration page.

------------

#### Main page (without country selected)
![main-page-without-country-selected](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/main_page_no_country_selected.png?raw=true)

This is the main page of the platform when you have no country selected. As you can see there are some features unavailable because they require a timezone which is automatically set based on your country selection.


------------

#### Main page (with country selected)
![main-page-without-country-selected](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/main_page_country_selected.png?raw=true)

After selecting a country, you will have full access to the application. Besides the features that became available to you, there is a calendar where you will see every day colored differently based on the tasks deadline. The color is more intense as you have more tasks with the deadline set to a certain day. You can view the current year or the next year deadlines calendar.

------------

#### My Account page
![user-profile](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/user_profile.png?raw=true)

This is the page where you can edit your account details.  The editable attributes of your user profile are: profile picture, country, description.

![edit-user-profile](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/edit_account.png?raw=true)

Below is an image with the account details after editing them.

![account-modified](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/account_modified.png?raw=true)

From this page you can also view and manage your friend requests.

![friend-requests-inbox](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/friend-requests-inbox.png?raw=true)

------------

#### To-do App pages
![tasks-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/tasks_1.png?raw=true)

Here is the place where you can manage your tasks. You can create, update, delete or filter them. By default, the newest created tasks are displayed first and the completed ones last.

![create-task-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create_task_1.png?raw=true)

![create-task-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create_task_2.png?raw=true)

![create-task-3](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create_task_3.png?raw=true)

![create-task-4](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create_task_4.png?raw=true)

![tasks-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/tasks_2.png?raw=true)

![tasks-3](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/tasks_3.png?raw=true)

![edit-task](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/edit_task.png?raw=true)

After you add some tasks, you will notice that the deadlines calendar from main page will get updated. The colors will change as you add more tasks with the deadline on the same day.

![deadlines-calendar-update-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/main_page_deadlines_1.png?raw=true)

![deadlines-calendar-update-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/main_page_deadlines_2.png?raw=true)

You can also view the next year status of deadlines calendar.

![deadlines-calendar-next-year](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/main_page_next_year.png?raw=true)

