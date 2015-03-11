import datetime

from django.db import models
from datetime import date, datetime
from random import randrange
from django.contrib.auth import hashers
from django.utils import timezone
import uuid

class User(models.Model):
    birthdate = models.DateField('someones birthday')
    random_number = models.IntegerField('bizzbuzz randomly generated number')
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=150, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=55, blank=True, null=True)
    lastname = models.CharField(max_length=75, blank=True, null=True)
    forgot_password_date = models.DateTimeField('The date someone initiates the password request', null=True)
    forgot_password_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email_address + ' ' + str(self.random_number) + ' ' + str(self.id)

    def get_age(self):
        today = date.today()
        birthday_in_future = 1
        if (today.month >= self.birthdate.month) and (today.day >= self.birthdate.day):
            birthday_in_future = 0

        return today.year - self.birthdate.year - birthday_in_future

    def get_birthdate_str(self):
        if self.birthdate is None:
            return ''
        return self.birthdate.strftime('%m/%d/%Y')

    def set_random_number(self):
        self.random_number = randrange(1, 100)

    def set_forgot_password(self):
        self.forgot_password_date = datetime.now()
        self.forgot_password_code = str(uuid.uuid1())

    def is_valid_password(self, password1, password2):
        if password1 == password2 and len(password1) > 6:
            return True
        return False

    def set_password(self, new_password):
        # should look into using a library for this instead such as bcrypt with stand
        salt = str(self.random_number)  # this is probably not a great salt; should create a separate salt field
        # self.password = hashlib.sha512(new_password + salt).hexdigest()
        self.password = hashers.make_password(new_password, salt, hasher='default')

    def check_login_password(self, verify_password):
        return hashers.check_password(verify_password, self.password)

    # Checks to see if the password request is still valid; within a date/time range and if the code has been used
    def is_password_request_valid(self):
        if self.forgot_password_code == '':
            return False
        return True
