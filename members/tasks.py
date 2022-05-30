import logging
from typing import List, Dict

from background_task import background
from django.core.exceptions import ValidationError

from .models import MemberAccount

logger = logging.getLogger()


@background(queue='create_member_accounts')
def create_member_accounts(member_accounts: List[Dict]):
    logger.info(f"Creating Member Accounts")
    member_account_objs = [MemberAccount(**ma) for ma in member_accounts]
    valid_objs = []
    for ma in member_account_objs:
        try:
            ma.clean_fields()
            ma.clean()
            valid_objs.append(ma)
        except ValidationError:
            logger.error("Found ValidationError when trying to create_member_account")

    MemberAccount.objects.bulk_create(valid_objs, ignore_conflicts=True)
    # Note, we could find the objects that were created (i.e. using an indexed created_at field)
    # and find the records we didn't create or update so we can report on them. This
    # was not part of the requirements and is possible a system can already have a sufficient
    # reporting mechanism (i.e. checks against a data warehouse).
    # Sidenote: we need to be mindful about how we log PII.


