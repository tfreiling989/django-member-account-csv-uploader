from django.core.validators import RegexValidator
from django.db import models


class MemberAccount(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=25)
    phone_regex = RegexValidator(regex=r'^\d{10}$',
                                 message="Phone number must be entered in the format: '9999999999'. Exactly 10 digits "
                                         "are required.")
    phone_number = models.CharField(validators=[phone_regex],max_length=10)
    client_member_id = models.CharField(max_length=7)
    account_id = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client_member_id', 'account_id'], name='unique client_member per account'),
            models.UniqueConstraint(fields=['phone_number', 'account_id'], name='unique phone_number per account')
        ]