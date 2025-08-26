from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20, null=True, blank=True)

    image = models.ImageField(upload_to='profile_images',
                              null=True, blank=True,
                              default='profile_images/default.png'
                              )


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']

    def __str__(self):
        return self.email