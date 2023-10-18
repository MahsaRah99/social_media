from django.db import models
from uuid import uuid4
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    class Meta:
        abstract = True


class MyManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_active=True)

    def archieves(self):
        return super().get_queryset().filter(is_active=False)


class SoftDeleteModel(BaseModel):
    objects = MyManager
    
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)
    
    def delete(self):
        self.is_active = False
        self.save()
        
    class Meta:
        abstract = True


class TimeStampMixin:
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)