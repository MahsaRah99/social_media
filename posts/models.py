from django.db import models
from core.models import BaseModel, SoftDeleteModel, TimeStampMixin
from django.utils.translation import gettext_lazy as _
from Blaze.settings import AUTH_USER_MODEL
from django.urls import reverse
from django.db.models import Manager


class Tag(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name

    def tag_post_count(self):
        return self.posts.count()

