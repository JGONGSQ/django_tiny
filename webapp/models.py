from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BaseDataModel(models.Model):
    def get_field_names(self):
        return [field.name for field in self._meta.fields]

    def get_values(self):
        return [getattr(self, field) for field in self.get_field_names()]

    class Meta:
        abstract = True


class UserPermissionType(BaseDataModel):

    USER_TYPE_SUPER = 'SUPER'
    USER_TYPE_ADMIN = 'ADMIN'
    USER_TYPE_OFFICER = 'OFFICER'
    USER_TYPE_REGULAR = 'REGULAR'

    USER_TYPE = (
        (USER_TYPE_REGULAR, 'REGULAR'),
        (USER_TYPE_OFFICER, 'OFFICER'),
        (USER_TYPE_ADMIN, 'ADMIN'),
        (USER_TYPE_SUPER, 'SUPER'),
    )

    user = models.OneToOneField(User)
    type = models.CharField(max_length=32, choices=USER_TYPE, default=USER_TYPE_REGULAR)


