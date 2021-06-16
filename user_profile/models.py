from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name, team, job_role):
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, team=team, job_role=job_role)
        user.save()
        return user


class NewUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.EmailField(max_length=100, unique=True)
    team = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
