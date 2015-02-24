import datetime

from django.db import models
from datetime import date, datetime
from random import randrange
from django.utils import timezone

class User(models.Model):
    birthdate = models.DateField('someones birthday')
    random_number = models.IntegerField('bizzbuzz randomly generated number')

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
        self.random_number = randrange(1,100)
