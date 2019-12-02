"""
All the custom validators are to be placed here.
"""

from rest_framework.serializers import ValidationError


def validate_name(name):
    if len(name) < 3:
        raise ValidationError('Name should have at least 2 characters')

    chars = list(name)

    # names should contain only alphabets and spaces.
    for char in chars:
        if not ('a' <= char <= 'z') and not ('A' <= char <= 'Z') and char != ' ':
            raise ValidationError('Name should only contain alphabets and spaces')


def validate_phone(phone):
    if len(phone) < 10:
        raise ValidationError('Phone number should contain 10 digits')

    digits = list(phone)

    # phone number should contain digits only
    for digit in digits:
        if not ('0' <= digit <= '9'):
            raise ValidationError('Phone number should only contain numbers')


def validate_user_name(user_name):
    if len(user_name) < 4:
        raise ValidationError('Username should contain at least 4 characters')

    chars = list(user_name)

    # user_name should contain only alphabets and numbers
    for char in chars:
        if not ('a' <= char <= 'z') and not ('A' <= char <= 'Z') and not ('0' <= char <= '9'):
            raise ValidationError('Username should not contain any special characters')

    # user_name should contain at least one alphabet
    contains_char = False
    for char in chars:
        if ('a' <= char <= 'z') or ('A' <= char <= 'Z'):
            contains_char = True
            break

    if not contains_char:
        raise ValidationError('Username should contain at least one alphabet')


def validate_password(password):
    if len(password) < 8:
        raise ValidationError('Password must contain at least 8 characters')
    if len(password) > 15:
        raise ValidationError('password can have at most 15 characters')
