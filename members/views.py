import csv
import io
import logging

from django.core.exceptions import BadRequest
from django.http import HttpResponse
from django.views import View

from .serializers import MemberAccountSerializer
from .tasks import create_member_accounts

logger = logging.getLogger()
from django.apps import apps


def schedule_create_member_accounts_task(buffer):
    """ This is just a wrapper as a workaround for mocking tasks"""
    create_member_accounts(buffer)


class MemberAccountUploadView(View):

    def post(self, request):
        file = io.TextIOWrapper(request.FILES["file"].file)
        reader = csv.DictReader(file)
        heading = reader.fieldnames
        app_config = apps.get_app_config('members')
        logger.info(f"self.app_config.file_uploader_record_buffer: {app_config.file_uploader_record_buffer}")
        expected_heading = [f for f in MemberAccountSerializer.Meta.fields if f not in ['id', 'created_at']]
        if heading != expected_heading:
            raise BadRequest(f"Invalid heading: {heading}. Expected: {expected_heading}")
        buffer = []
        for row in reader:
            buffer.append(row)
            if len(buffer) >= app_config.file_uploader_record_buffer:
                schedule_create_member_accounts_task(buffer)
                buffer = []
        if buffer:
            schedule_create_member_accounts_task(buffer)
        return HttpResponse(status=204)

