import string
import random
from django.core.cache import cache
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
