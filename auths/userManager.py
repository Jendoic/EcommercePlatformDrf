from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser


class MyUserManager(UserManager):
    """
    Custom user model manager where email is the unique identifiers for authentication instead of usernames
    """

    def _create_user(self, email, password, **extra_fields ):
        """
        Create and save a user with the given email and password
        """
        if not email:
            raise ValueError('Email must be provided')
        
        email = self.model( email = self.normalize_email(email))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
       
    
    def create_user(self, email,password=None, **extrafields):
        extrafields.setdefault("is_staff", False)
        extrafields.setdefault("is_superuser", False)
        extrafields.setdefault("is_active", True)
        return self.create_user(email, password, **extrafields)


    def create_superuser(self, email,password=None, **extrafields):
        """
        Create and save a superuser with the given email and password.
        """

        extrafields.setdefault("is_staff", True)
        extrafields.setdefault("is_superuser", True)
        extrafields.setdefault("is_active", True)

        # if extra_fields.get("is_staff") is not True:
        #     raise ValueError(_("Superuser must have is_staff=True. "))
        
        # if extra_fields.get("is_superuser") is not True:
        #     raise ValueError(_("Superuser must have is_superuser=True. "))
        
        return self._create_user(email, password, **extrafields)


