* I am still working on readme file...*
# Efficient Study Platform

> *Motivation: I built this project because I wanted to learn a new web framework (Django)  and different kinds of tools and techniques related to full stack development. I chose the project topic guided by the wish of creating something that has a real life applicability and also that would help me.*

------------

## Table of contents
- [Description](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#description)
- [Project Features](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#project-features )
- [Project Presentation](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#project-presentation)
	- [Home](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#home-page)
	- [Registration](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#registration-page)
	- [Login](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#login-page)
	- [Forgot Password](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#forgot-password-page)
	- [Main (without country selected)](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#main-page-without-country-selected)
	- [Main (with country selected)](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#main-page-with-country-selected)
	- [My Account](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#my-account-page)
	- [To-Do App](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#to-do-app-pages)
	- [Flashcards App](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#flashcards-app-pages)
	- [Search Users](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#search-users-page)
	- [Collaborative Study Session](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#collaborative-study-session-app-pages)
- [Run](https://github.com/Alex-SA1/Efficient-Study-Platform?tab=readme-ov-file#run-locally-the-project)


### Description
The purpose of the application is to provide an online environment for students that will help them in the study process.

Navigating through the app you will find a tasks management system, a place for creating flashcards, the possibility of editing your own user profile and sending friend requests and also, a section where you can connect with your friends and start live chatting. If you are the kind of person that likes to study for fixed and organised periods of time, the pomodoro timer that you will find in the study session section may help you.

### Project Features
- Responsiveness (the website design is responsive for every device)
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

The first page that you will see when you enter on website. Here you will find just a presentation text and two buttons for accessing the register and login page.

![home-page](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/home_page.png?raw=true)

------------

#### Registration Page

![registration-page](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/register_page.png?raw=true)

Here you will find a registration form with the following field constraints (if the form is submitted with invalid data, you will be notified about it and the account won't be created):
- Username: should be unique
- Email: should be unique and valid
- Verification Code: should be equal with the one received on email
- Password: minimum 8 characters, not too similar to username and email, not a common password, not entirely numeric

This is how the verification mail sent to you would look like.
![registration-code](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/regsitration_code.png?raw=true)

Note: The email will be marked as spam because is sent from a testing email address and not from an oficial domain.

Below you will find an image with the registration form filled with data. The password is shown because I clicked on the eye icon.

![registration-form-filled](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/registration_form_filled.png?raw=true)

The verification code will be stored for 3 minutes in cache memory (Redis) and after that it will be deleted and no longer valid. It is associated with the email that you entered so any other code different from the one received on the mail will be invalid.

The password is hashed using SHA256 and stored in this way in the database.

------------

#### Login Page

You will be asked for your account username and password. You can click on eye icon and the password will be revelead for a few seconds. Also, you will find links to "Forgot Password" page and registration page.

![login-page](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/login_page.png?raw=true)

------------

#### Forgot Password Page

![forgot-password-page](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/reset-password.png?raw=true)

Here you can reset your account password.

The verification code system works similar to the one from registration process, but what is different here is the way by which the code is identified in the cache memory because it will be associated with the reset password process so that there are no collisions with the registration verification codes.

This is how the verification mail sent to you would look like.
![reset-password-code](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/password_reset_code.png?raw=true)

Note: The email will be marked as spam because is sent from a testing email address and not from an oficial domain.

Same constraints that are applied to the password in the registration form, are also applied when you want to reset the password.

------------

#### Main Page (without country selected)

This is the first page that you will be redirected to after logging in.

![main-page-without-country-selected](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/main_page_no_country_selected.png?raw=true)

By default, on your user profile you will not have a country selected so, as you can see some platform features are unavailable. To obtain full access to the application you have to set your country so that the app can identify your timezone and offer you a customized experience.

------------

#### Main Page (with country selected)

After selecting a country, you will have full access to the application. 

Besides the features that became available to you, there is a calendar where you will see every day colored differently based on the tasks deadline. The color is more intense as you have more tasks with the deadline set to a certain day. You can view the current year or the next year deadlines calendar.

![main-page-without-country-selected](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/main_page_country_selected.png?raw=true)

------------

#### My Account Page

Here you can view your account details.

![user-profile](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/user_profile.png?raw=true)

You can edit your account from a dedicated page that you can access by clicking on "edit account" button. 

The editable attributes of your user profile are: profile picture, country, description.

Profile picture has some validators that are checking for:
- extensions (.jpg, .jpeg, .png)
- image integrity
- image size (max. 2 mb)

Country has to be selected from a given list.

![edit-user-profile](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/edit_account.png?raw=true)

Below is an image with the account details after editing them.

![account-modified](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/account_modified.png?raw=true)

From this page you can also view and manage your friend requests.

![friend-requests-inbox](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/friend-requests-inbox.png?raw=true)

------------

#### To-do App Pages
![tasks-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/tasks_1.png?raw=true)

Here is the place where you can manage your tasks. You can create, update, delete or filter them. By default, the newest created tasks are displayed first and the completed ones last.

![create-task-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create_task_1.png?raw=true)

![create-task-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create_task_2.png?raw=true)

![create-task-3](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create_task_3.png?raw=true)

![create-task-4](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create_task_4.png?raw=true)

![tasks-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/tasks_2.png?raw=true)

![tasks-3](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/tasks_3.png?raw=true)

![edit-task](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/edit_task.png?raw=true)

![delete-task](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/delete-task.png?raw=true)

After you add some tasks, you will notice that the deadlines calendar from main page will get updated. The colors will change as you add more tasks with the deadline on the same day.

![deadlines-calendar-update-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/main_page_deadlines_1.png?raw=true)

![deadlines-calendar-update-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/main_page_deadlines_2.png?raw=true)

You can also view the next year status of deadlines calendar.

![deadlines-calendar-next-year](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/main_page_next_year.png?raw=true)

------------

#### Flashcards App Pages

This is the place for managing your flashcards.

![flashcards-folders-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/flashcards-folders-1.png?raw=true)

The flashcards are stored in folders.

![create-folder](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create-folder.png?raw=true)

![flashcards-folders-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/flashcards-folders-2.png?raw=true)

![create-flashcard-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create-flashcard-1.png?raw=true)

![create-flashcard-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create-flashcard-2.png?raw=true)

![create-flashcard-3](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create-flashcard-3.png?raw=true)

You can reverse the card by clicking on it.

![create-flashcard-4](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/create-flashcard-4.png?raw=true)

After creating a flashcard, the flashcards counter for the corresponding folder will be updated.

![flashcards-counter-updated](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/flashcards-counter-updated.png?raw=true)

You can also update/delete a folder or a flashcard. If you delete a folder, all flashcards stored in it will be also deleted.

![update-folder](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/update-folder.png?raw=true)

![delete-folder](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/delete-folder.png?raw=true)

By default the action buttons for flashcards are hidden and you have to display them if you want to edit/delete a flashcard.

![show-flashcards-actions](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/view-flashcards-actions.png?raw=true)

![update-flashcard](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/update-flashcard.png?raw=true)

![delete-flashcard](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/delete-flashcard.png?raw=true)

To view the flashcards from a folder you have to click on the folder and after that you can click on any flashcard to reverse it.

![view-flashcard-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/view-flashcards-1.png?raw=true)

![view-flashcard-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/view-flashcard-2.png?raw=true)

------------

#### Search Users Page

In this section you can search for users, view their profile or send a friend request.

![search-users-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/search-users-1.png?raw=true)

![search-users-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/search-users-2.png?raw=true)

![view-user-profile](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/view-user-profile.png?raw=true)

![friend-request-sent](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/friend-request-sent.png?raw=true)

After sending a friend request to a user, he will get notified when logs in. Also, the friend request will be displayed in his inbox.

![friend-request-notification](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/friend-request-notification.png?raw=true)

![friend-requests-inbox-updated](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/friend-requests-inbox-updated.png?raw=true)

------------

#### Collaborative Study Session App Pages

This is the place where you can create/join study sessions and start learning together with your friends.

![join-study-session](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/join-study-session.png?raw=true)

![study-session-1](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/study-session-1.png?raw=true)

You can copy the study session code to clipboard.

![study-session-code](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/study-session-code.png?raw=true)

![study-session-2](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/study-session-2.png?raw=true)

![study-session-3](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/study-session-3.png?raw=true)

You can edit pomodoro timer minutes.

![pomodoro-timer-settings](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/pomodoro-timer-settings.png?raw=true)

The timer circle gets updated as time elapses and it resets for every cycle change.

![pomodoro-timer-circle](https://github.com/Alex-SA1/Efficient-Study-Platform/blob/main/images/pomodoro-timer-circle.png?raw=true)

## Run locally the project

- Clone my repository on your machine
- Create a .env file with the same format as .env.example in the same directory and fill the values in .env according to the explanations from example file
- To obtain a Django secret key you can search on Google for a generator
- To obtain a Mailjet API key you have to create an account (free plan) on the platform and copy the required values from the admin dashboard
- To obtain a Cloudinary API key you have to create an account (free plan) on the platform and copy the required values from the admin dashboard
- Make sure that .env file has only LF (not CRLF as on Windows) for new lines (you can check that from Visual Studio Code)
- Make sure the ports 3306 and 6379 have no services running on them (you can check that from Services on Windows)
- Run the following command in the root directory:

```bash
  docker compose up --build
```
- After completing all these steps, you should have the website live on your localhost
    