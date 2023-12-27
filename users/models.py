from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_("Email Address"),
        unique=True,
        help_text=_("Required. Enter a valid email address."),
    )
    bio = models.CharField(
        verbose_name=_("Biograpghy"),
        max_length=300,
        blank=True,
        help_text=_("Optional. Enter a brief description about yourself."),
    )
    location = models.CharField(
        verbose_name=_("Location"),
        max_length=100,
        blank=True,
        help_text=_("Optional. Enter your living location."),
    )
    picture = models.FileField(
        upload_to="profiles/%Y/%m/%d/",
        blank=True,
        help_text=_("Optional. Upload a profile picture."),
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    is_admin = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def followings_count(self) -> int:
        return self.followings.count()

    @property
    def followers_count(self) -> int:
        return self.followers.count()

    def get_followers(self):
        return self.followers.all()

    def get_followings(self):
        return self.followings.all()


class Relation(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followings"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )

    def __str__(self) -> str:
        return f"{self.from_user} follows {self.to_user}"
