from django.core.cache import cache
from django.utils import timezone
from .models import Task, StudySessionMessage, FriendRequest, Friendship, FlashcardsFolder
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
import string
import random
import json
import pickle


def generate_verification_code():
    """
    helper function that generates a verification code for the mail verification process
    """
    letters = string.ascii_lowercase + string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    # creating a list with all characters that can be used in the verification code
    available_characters = list(letters + digits + special_characters)

    # shuffle the list with all characters for more randomness
    random.shuffle(available_characters)

    # the verification code will have 8 characters
    code = ""
    for _ in range(8):
        random_index = random.randint(0, len(available_characters) - 1)
        code += available_characters[random_index]

    return code


def save_verification_code(record_key: string, record_value: string):
    """
    helper function that saves in cache memory the verification code sent via email to the user 
    """

    # the verification code will be available for just 3 minutes (180 seconds)
    cache.set(record_key, record_value, timeout=180)


def check_verification_code(verification_code: string, expected_verification_code_key: string) -> bool:
    """
    helper function that checks if the verification code entered by the user is the expected verification code
    raises Exception if the verification code is not right
    """

    # retrieving the verification code sent to the user from the cache memory (where it was stored temporary)
    expected_verification_code = cache.get(expected_verification_code_key)

    if verification_code != expected_verification_code:
        raise Exception("Wrong verification code!")


def delete_verification_code(record_key: string):
    """
    helper function that deletes the registration stored in cache memory with a given key
    this function is intended to be called when it is needed to delete a verification code for certain email from cache memory
    """

    try:
        cache.delete(record_key)
    except:
        return


def filter_tasks_by_deadline_date(tasks: QuerySet, deadline_date: string):
    """
    helper function that filters the tasks received as parameter by a given deadline date
    """
    filtered_tasks_pks = []

    for task in tasks:
        deadline_field = str(timezone.localtime(getattr(task, 'deadline')))
        if deadline_date in deadline_field:
            filtered_tasks_pks.append(task.pk)

    return tasks.filter(pk__in=filtered_tasks_pks)


def valid_study_session(session_code: string) -> bool:
    """
    helper function that checks if the given session code corresponds to a valid study session
    returns True if there is a valid study session with the given code or False otherwise
    """

    return cache.get(session_code) is not None


def register_study_session(session_code: string, username: string):
    """
    helper function that registers in cache memory a study session

    username: the username of the user that created the study session
    """
    cache.set(session_code, [username], timeout=None)


def add_user_to_study_session(session_code: string, username: string):
    """
    helper function that adds a user to a study session

    precondition: the given session code corresponds to a valid study session
    """
    users = cache.get(session_code, [])

    if username not in users:
        users.append(username)
        cache.set(session_code, users, timeout=None)


def remove_user_from_study_session(session_code: string, username: string):
    """
    helper function that removes a user from a study session

    precondition: the given session code corresponds to a valid study session
    """
    users = cache.get(session_code, [])

    users.remove(username)
    cache.set(session_code, users, timeout=None)


def study_session_empty(session_code: string) -> bool:
    """
    helper function that checks if a study session is empty (if there are no users in session)
    """
    users = cache.get(session_code, [])

    return len(users) == 0


def delete_study_session_chat_history(session_code: string):
    """
    helper function that deletes all messages saved for a study session chat
    """
    StudySessionMessage.objects.filter(
        group_name=f"study_session_{session_code}").delete()


def remove_study_session(session_code: string):
    """
    helper function that removes a study session

    precondition: the given session code corresponds to a valid study session
    """
    study_session_group_key = f"asgi:group:study_session_{session_code}"

    cache.delete(session_code)
    cache.delete(study_session_group_key)
    delete_study_session_chat_history(session_code)


def get_friend_request(user_1: User, user_2: User):
    """
    helper function that checks if there is a friend request between two users
    returns the friend request object, if there is a friend request between the users, or None otherwise

    precondition: user_1 and user_2 are both valid users
    """

    # first search: user_1 as sender, user_2 as receiver
    try:
        friend_request = FriendRequest.objects.get(
            sender=user_1, receiver=user_2)
    except:
        # second search: user_2 as sender, user_1 as receiver
        try:
            friend_request = FriendRequest.objects.get(
                sender=user_2, receiver=user_1)
        except:
            return None

    return friend_request


def check_friendship(user_1: User, user_2: User):
    """
    helper function that checks if two given users are friends

    precondition: user_1 and user_2 are both valid users
    """
    friends = False

    try:
        friendship = Friendship.objects.get(user_1=user_1, user_2=user_2)
        friends = True
    except:
        try:
            friendship = Friendship.objects.get(user_1=user_2, user_2=user_1)
            friends = True
        except:
            friends = False

    return friends


def check_pending_friend_request(sender_user: User, receiver_user: User):
    """
    helper function that checks if there is a friend request in pending sent by sender_user to receiver_user

    precondition: sender_user and receiver_user are both valid users
    """

    found = False

    try:
        friend_request = FriendRequest.objects.get(
            sender=sender_user, receiver=receiver_user, status='pending')

        found = True
    except:
        found = False

    return found


def increment_folder_flashcards_number(folder: FlashcardsFolder):
    """
    helper function that increments by 1 the flashcards number of a given folder

    precondition: folder is a valid FlashcardsFolder
    """

    new_folder_flashcards_number = folder.flashcards_number + 1
    setattr(folder, "flashcards_number", new_folder_flashcards_number)
    folder.save()


def decrement_folder_flashcards_number(folder: FlashcardsFolder):
    """
    helper function that decrements by 1 the flashcards number of a given folder

    precondition: folder is a valid FlashcardsFolder, folder.flashcards_number > 0
    """

    new_folder_flashcards_number = folder.flashcards_number - 1
    setattr(folder, "flashcards_number", new_folder_flashcards_number)
    folder.save()


def joined_in_study_session(username: string, session_code: string) -> bool:
    """
    helper function that checks if a user is joined in a study session

    precondition: username corresponds to a valid user and session code corresponds to a valid study session
    """
    users = cache.get(session_code, [])
    
    return username in users


def allowed_to_study_session(username: string, session_code: string) -> bool:
    """
    helper function that checks if a user is allowed to join a study session
    a user is allowed to join a study session only if he is friend with at least one of the study session participants

    precondition: username corresponds to a valid user and session code corresponds to a valid study session
    """
    allowed = False
    users = cache.get(session_code, [])

    for current_username in users:
        user_to_check = User.objects.get(username=username)
        current_user = User.objects.get(username=current_username)
        if check_friendship(user_to_check, current_user):
            allowed = True

    return allowed
