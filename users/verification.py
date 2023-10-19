from django.db import models
from core.models import BaseModel, TimeStampMixin

class OtpCode(BaseModel, TimeStampMixin):
	email = models.EmailField(unique=True)
	code = models.PositiveSmallIntegerField()

	def __str__(self):
		return f'{self.email} - {self.code} - {self.created_at}'