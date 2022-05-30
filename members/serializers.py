from rest_framework import serializers
from .models import MemberAccount


class MemberAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberAccount
        fields = ('id',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'client_member_id',
                  'account_id',
                  'created_at')
