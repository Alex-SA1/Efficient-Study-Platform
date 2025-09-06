from django import template
from ..utils import check_friendship, check_pending_friend_request

register = template.Library()


@register.simple_tag(name="is_friend")
def is_friend(session_user, user):
    """
    check if the user from the current session is friend with a given user

    session_user: user from the current session
    user: a given user

    precondition: session_user and user are both valid users
    """
    return check_friendship(session_user, user)


@register.simple_tag(name="pending_friend_request")
def pending_friend_request(user_1, user_2):
    """
    check if there is a friend request in pending sent by user_1 to user_2

    session_user: user from the current session
    user: a given user

    precondition: session_user and user are both valid users
    """
    return check_pending_friend_request(user_1, user_2)
