from django.db import models
from django.contrib.auth.models import AbstractUser
from users.validators import validate_phone


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20, null=True, blank=True, validators=[validate_phone])

    image = models.ImageField(upload_to='profile_images',
                              null=True, blank=True,
                              default='profile_images/default.png'
                              )

    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']

    def __str__(self) -> str:
        return self.email