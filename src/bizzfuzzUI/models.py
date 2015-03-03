import datetime

from django.db import models
from datetime import date, datetime
from random import randrange
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
        return self.random_number

    def get_age(self):
        today = date.today()
        birthday_in_future = 1
        if (today.month >= self.birthdate.month) and (today.day >= self.birthdate.day) :
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
        self.forgot_password_code = uuid.uuid1()

    # Checks to see if the password request is still valid; within a date/time range and if the code has been used
    def is_password_request_valid(self):
        if self.forgot_password_code == '':
            return False
        return True
