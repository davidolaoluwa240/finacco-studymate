from django.db import models
from django.contrib.auth.models import AbstractUser

'''
    User Custom Model
'''
class User(AbstractUser):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Biweekly'),
        ('monthly', 'Monthly'),
        ('never', 'Never'),
    ]

    email = models.EmailField(unique=True)
    avatar = models.ImageField(default='avatar.svg', blank=True, null=True)
    email_frequency = models.CharField(max_length=10,
        choices= FREQUENCY_CHOICES,
        default='weekly',
        help_text="How often do you want to receive study summary emails?")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + ' ' + self.last_name

'''
    Exam Model
'''
class Exam(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

'''
    Session Model
'''
class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    duration = models.DurationField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", '-created']

    def __str__(self):
        return self.name

'''
    Session Note Model
'''
class SessionNote(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    note = models.TextField()
    image = models.ImageField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", '-created']

    def __str__(self):
        return self.note[0:50]