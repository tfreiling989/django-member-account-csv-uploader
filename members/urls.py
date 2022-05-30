from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from .views import MemberAccountUploadView
from .viewsets import (
    MemberAccountViewSet
)

router = DefaultRouter()

BASENAME = "basename"

router.register(r"", MemberAccountViewSet, **{BASENAME: "memberaccount"})

urlpatterns = router.urls + [
    path('importcsv', csrf_exempt(MemberAccountUploadView.as_view()), name='importmemberscsv')
]