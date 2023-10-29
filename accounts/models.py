from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from ecommerce import settings
from utilities.models import City, State, TimestampedModel, mobile_regex, pincode_regex
from versatileimagefield.fields import PPOIField, VersatileImageField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'ec_users'
        verbose_name_plural = 'Users'

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email


class CustomUserDetail(TimestampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    mobile_number = models.CharField(
        max_length=10, unique=True, validators=[mobile_regex])
    avatar = VersatileImageField('Avatar',
                                 upload_to='accounts/avatars', null=True, blank=True)
    ppoi = PPOIField('Image PPOI')

    class Meta:
        db_table = 'ec_user_details'
        verbose_name_plural = 'User Details'

    def __str__(self) -> str:
        return self.username


class CustomUserAddress(TimestampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='user_addresses')
    name = models.CharField(max_length=75)
    phone = models.CharField(max_length=10, validators=[mobile_regex])
    pin_code = models.CharField(max_length=6, validators=[pincode_regex])
    locality = models.CharField(max_length=75)
    address = models.TextField()
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='user_addresses')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='user_addresses')
    landmark = models.CharField(max_length=50, null=True, blank=True)
    alternate_number = models.CharField(
        max_length=10, null=True, blank=True, validators=[mobile_regex])

    class Meta:
        db_table = 'ec_user_addresses'
        verbose_name_plural = 'User Addresses'

    def __str__(self) -> str:
        return f'{self.user.email} - {self.name}'
