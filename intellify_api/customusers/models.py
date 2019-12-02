from django.db import models
from django.core.validators import ValidationError
from customusers.validators import validate_name, validate_phone, validate_user_name, validate_password
from customusers.functions import encrypt_password


class CustomUser(models.Model):
    name = models.CharField(max_length=40, validators=[validate_name])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, validators=[validate_phone], null=True,
                             blank=True, unique=True, verbose_name='phone number')
    user_name = models.CharField(max_length=15, unique=True, validators=[validate_user_name],
                                 primary_key=True)
    password = models.CharField(max_length=300)
    created_on = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['user_name']
        verbose_name = 'user'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, new_password=False):
        if new_password:
            validate_password(self.password)
            self.password = encrypt_password(self.password)
        super(CustomUser, self).save()
