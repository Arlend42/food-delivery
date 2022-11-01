from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManger(BaseUserManager):  # only contains methods
    def create_user(self, first_name, last_name, user_name, email, password=None):
        if not email:
            return ValueError('Email is required!')
        
        if not user_name:
            return ValueError('Username is required!')

        user = self.model( 
            email=self.normalize_email(email),
            user_name=user_name,
            first_name=first_name,
            last_name=last_name
        )
        
        user.set_password(password)
        user.save(using=self.db)    # in that you have many databases you can use this using built-in
        return user

    def create_superuser(self, first_name, last_name, user_name, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            user_name=user_name,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )  # we need a user in order to create a superuser
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user
 

class User(AbstractBaseUser):
    RESTAURANT = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (RESTAURANT, 'Restaurant'),
        (CUSTOMER, 'Customer')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    #  Rquired fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    objects = UserManger

    def __str__(self):
        return self.email

    def has_permission(self, permission, obj=None):
        return self.is_admin

    def has_module_permission(self, app_label):
        return True
