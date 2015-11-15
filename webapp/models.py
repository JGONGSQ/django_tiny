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


class Permission(BaseDataModel):
    """
        This is the user permission model, to define the user is an officer or not.
    """
    TYPE_SUPER = 'SUPER'
    TYPE_ADMIN = 'ADMIN'
    TYPE_OFFICER = 'OFFICER'
    TYPE_REGULAR = 'REGULAR'
    # TYPE_CUSTOMER = 'CUSTOMER'
    # TYPE_PROVIDER = 'PROVIDER'

    TYPE = (
        (TYPE_REGULAR, 'REGULAR'),
        (TYPE_OFFICER, 'OFFICER'),
        (TYPE_ADMIN, 'ADMIN'),
        (TYPE_SUPER, 'SUPER'),
    )

    user = models.OneToOneField(User)
    type = models.CharField(max_length=32, choices=TYPE, default=TYPE_REGULAR)


class UserExtends(BaseDataModel):
    TYPE_MALE = 'Male'
    TYPE_FEMALE = 'Female'

    GENDER_TYPE = (
        (TYPE_MALE, 'Male'),
        (TYPE_FEMALE, 'Female'),
    )

    user = models.OneToOneField(User)
    gender = models.CharField(max_length=32, choices=GENDER_TYPE)
    dob = models.DateField()


class Space(BaseDataModel):
    """
        Space for user
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    size = models.IntegerField(default=0)


class Diary(BaseDataModel):
    """
        Diary for space
    """
    space = models.ForeignKey(Space)
    title = models.CharField(max_length=128)
    content = models.TextField()
    image = models.ImageField()
