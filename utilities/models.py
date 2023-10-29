from django.core.validators import RegexValidator
from django.db import models

# Validators
mobile_regex = RegexValidator('(?!([\d])\1{9})[6789]\d{9}$', 'Number invalid!')
pincode_regex = RegexValidator('^[1-9][0-9]{5}$', 'Pincode invalid!')


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class State(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'ec_states'
        verbose_name_plural = 'States'

    def __str__(self) -> str:
        return self.name


class City(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        db_table = 'ec_cities'
        verbose_name_plural = 'Cities'

    def __str__(self) -> str:
        return self.name
