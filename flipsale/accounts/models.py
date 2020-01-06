from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class UserManager(BaseUserManager):
    #python manage.py createuser
    def create_user(self, email, mobile, full_name, password=None,  is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not mobile:
            raise ValueError("Users must have a mobile number")
        if not full_name:
            raise ValueError("Users must have a full name")

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.mobile = mobile
        user_obj.full_name = full_name
        user_obj.save(using=self._db)
        return user_obj

    #python manage.py createstaffuser
    def create_staffuser(self, email, mobile, full_name, password=None):
        user = self.create_user(
                email,
                password=password,
                mobile=mobile,
                full_name = full_name,
                is_staff=True
        )
        return user

    #python manage.py createsuperuser
    def create_superuser(self, email, mobile, full_name, password=None):
        user = self.create_user(
                email,
                password=password,
                mobile=mobile,
                full_name = full_name,
                is_staff=True,
                is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True)
    full_name   = models.CharField(max_length=255, blank=True, null=True)
    mobile      = models.BigIntegerField()
    active      = models.BooleanField(default=True) # can login 
    staff       = models.BooleanField(default=False) # staff user non superuser
    admin       = models.BooleanField(default=False) # superuser 
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['full_name', 'mobile'] #python manage.py createsuperuser

    objects = UserManager()
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        "This will perform get, set and del of staff"
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    #solves error of has_module_perms
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


