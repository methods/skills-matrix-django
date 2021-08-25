from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from .validators import validate_domain_email


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, surname, team, job_role, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_supersuser=True.')

        if other_fields.get('is_admin') is not True:
            raise ValueError('Superuser must be assigned to is_admin=True.')

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        user = self.create_user(email=self.normalize_email(email), first_name=first_name, surname=surname, team=team,
                                job_role=job_role, password=password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, first_name, surname, team, job_role, password, **other_fields):

        if not email:
            raise ValueError('You must provide and email address')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, surname=surname, team=team, job_role=job_role,
                          password=password, **other_fields)
        user.save()
        return user


class NewUser(AbstractBaseUser):
    email = models.EmailField(validators=[validate_domain_email], unique=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'surname', 'team', 'job_role']

    def __str__(self):
        return f'{self.first_name} {self.surname}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def update_from_request(self, form_data):
        for field_name in ['email', 'first_name', 'surname', 'team', 'job_role']:
            if field_name in form_data:
                setattr(self, field_name, form_data[field_name])
        self.save()
