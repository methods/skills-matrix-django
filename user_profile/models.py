from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name, surname, team, job_role, password):
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, surname=surname, team=team, job_role=job_role,
                          password=password)
        user.save()
        return user


class NewUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.email}, {self.first_name}, {self.team}, {self.job_role}"
