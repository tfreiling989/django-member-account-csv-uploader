from django.apps import AppConfig
import os
import environ
env = environ.Env()


class MembersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'members'
    file_uploader_record_buffer = env.int("MEMBER_ACCOUNT_FILE_UPLOADER_RECORD_BUFFER",100000)
