from django import forms
from .models import MemberAccount


class MemberAccountModelForm(forms.ModelForm):
    class Meta:
        model = MemberAccount
        fields = ('first_name',
                  'last_name',
                  'phone_number',
                  'client_member_id',
                  'account_id')

