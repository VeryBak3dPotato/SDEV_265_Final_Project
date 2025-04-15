# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, firstName, lastName, zipCode, password, **extra_fields):
#         if not email:
#             raise ValueError('A valid email address is required')

#         email = self.normalize_email(email)
#         user = self.model(email=email, firstName=firstName, lastName=lastName, zipCode=zipCode, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, firstName, lastName, zipCode, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True')

#         return self.create_user(email, firstName, lastName, zipCode, password, **extra_fields)

# class User(AbstractUser, PermissionsMixin):
#     firstName = models.CharField(max_length=25, blank=True)
#     lastName = models.CharField(max_length=25, blank=True)
#     email = models.EmailField(unique=True)
#     zipCode = models.CharField(max_length=5, blank=True)

#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
    
#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['firstName', 'lastName']

#     def __str__(self):
#         return self.email