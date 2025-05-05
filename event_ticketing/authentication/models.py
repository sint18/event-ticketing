from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "User"),
        ("organizer", "Organizer"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    email = models.EmailField(unique=True, blank=False, null=False)
    REQUIRED_FIELDS = []
    # Set email as the USERNAME_FIELD for Django's auth system
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # Add related_name to avoid conflicts if you are using permissions or groups
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="user",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="user",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def is_organizer(self):
        return self.role == "organizer"

    def is_user(self):
        return self.role == "user"
