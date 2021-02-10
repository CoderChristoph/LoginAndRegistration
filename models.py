from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class RegistrationManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # First Name Validation
        if len(postData['fName']) < 1:
            errors['first_name'] = "Required Field!"
        elif len(postData['fName']) < 2:
            errors['first_name'] = "First name must have 2 or more characters"
        elif postData['fName'].isalpha() == False:
            errors['first_name'] = "First name must only contain letters!"

        # Last Name Validation
        if len(postData['lName']) < 1:
            errors['last_name'] = 'Required Field!'
        elif len(postData['lName']) < 2:
            errors['last_name'] = "Last name must have 2 or more characters"
        elif postData['lName'].isalpha() == False:
            errors['last_name'] = "Last name must only contain letters!"

        # Email Validation
        if len(postData['email']) < 1:
            errors['email'] = "Required Field!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email!"
        existing_users = Registration.objects.filter(email=postData['email'])
        if len(existing_users) > 0:
            errors['email'] = "That email already exists!"

        # Password Validation
        if len(postData['password']) < 1:
            errors['password'] = "Required Field"
        elif len(postData['password']) < 8:
            errors['password'] = "The password must contain 8 characters or more!"
        else:
            if postData['password'] != postData['confirmPW']:
                errors['confirmPW'] = "The passwords do not match!"

        return errors


class Registration(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RegistrationManager()