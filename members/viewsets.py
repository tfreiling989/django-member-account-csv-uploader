
from .models import MemberAccount
from .serializers import MemberAccountSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend


class StandardResultsSetPagination(LimitOffsetPagination):
    max_limit = 1000


class MemberAccountViewSet(ModelViewSet):
    """Member Accounts ViewSet"""
    queryset = MemberAccount.objects.all()
    serializer_class = MemberAccountSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'account_id','phone_number','client_member_id']
    pagination_class = StandardResultsSetPagination
