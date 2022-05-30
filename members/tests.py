import csv
from typing import List, Tuple, Dict, Optional
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from .tasks import create_member_accounts


# Create your tests here.

@mock.patch('members.views.schedule_create_member_accounts_task', side_effect=create_member_accounts.now)
class MemberAccountUploadViewTestCase(TestCase):
    VALID_HEADERS = ('first_name', 'last_name', 'phone_number', 'client_member_id', 'account_id')

    @staticmethod
    def create_record_row(account_id=1, phone_number=1234567890, client_member_id=1234) -> Tuple:
        return ('Joe', 'Dirt', str(phone_number), str(client_member_id), str(account_id))

    @staticmethod
    def _add_header_to_rows(rows: List[List[str]], headers: List[str] = VALID_HEADERS) -> List[List[str]]:
        return [headers] + [r for r in rows]

    @staticmethod
    def _write_and_retrieve_file(rows: List[List[str]]) -> SimpleUploadedFile:
        file_name = "test.csv"
        # Open file in write mode (Arrange)
        with open(file_name, "w") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
        # open file in read mode
        with open(file_name, "rb") as data_to_read:
            # Create a simple uploaded file
            file = SimpleUploadedFile(
                content=data_to_read.read(), name=data_to_read.name, content_type="multipart/form-data"
            )
        return file

    @staticmethod
    def _call_import_csv_api(client, file):
        data = {'file': file}
        return client.post('/members/importcsv', data)

    def _verify_records(self, raw_inputs: List[List], result_dicts: List[Dict]):
        self.assertEqual(len(raw_inputs),len(result_dicts))
        for i in range(len(raw_inputs)):
            raw_input = raw_inputs[i]
            result_dict = result_dicts[i]
            self.assertEqual(raw_input[0], result_dict["first_name"])
            self.assertEqual(raw_input[1], result_dict["last_name"])
            self.assertEqual(raw_input[2], result_dict["phone_number"])
            self.assertEqual(raw_input[3], result_dict["client_member_id"])
            self.assertEqual(raw_input[4], result_dict["account_id"])

    def _common_flow(self,raw_inputs:List,expected_raw_inputs:Optional[List] = None,headers = VALID_HEADERS, expected_error_code: Optional[int] = None):
        client = Client()
        file = self._write_and_retrieve_file(self._add_header_to_rows(raw_inputs,headers))
        resp = self._call_import_csv_api(client, file)
        if expected_error_code:
            self.assertEqual(resp.status_code, expected_error_code)
        else:
            member_accounts_resp = client.get("/members/")
            self.assertEqual(member_accounts_resp.status_code, 200)
            member_accounts = member_accounts_resp.json()["results"]
            print(f"Received member_accounts: {member_accounts}")
            self._verify_records(expected_raw_inputs, member_accounts)

    def test_bulk_upload_happy_path(self,_):
        records_raw = [self.create_record_row(i) for i in range(5)]
        self._common_flow(records_raw,records_raw)

        more_records = [self.create_record_row(i) for i in range(5,10)]
        mix = [records_raw[0]] + more_records
        records_total = records_raw + more_records
        self._common_flow(mix, records_total)

    def test_bulk_upload_happy_path(self,_):
        records_raw = [self.create_record_row(i) for i in range(5)]
        self._common_flow(records_raw,records_raw)

        more_records = [self.create_record_row(i) for i in range(5,10)]
        mix = [records_raw[0]] + more_records
        records_total = records_raw + more_records
        self._common_flow(mix, records_total)

    def test_bulk_upload_same_phone_number_and_account(self,_):
        records_raw = [
            self.create_record_row(account_id=1,phone_number=9087654321,client_member_id=1234),
            self.create_record_row(account_id=1, phone_number=9087654321, client_member_id=4321)
        ]
        self._common_flow(records_raw,[records_raw[0]])

    def test_bulk_upload_same_client_member_id_and_account(self,_):
        records_raw = [
            self.create_record_row(account_id=1,phone_number=9087654321,client_member_id=1234),
            self.create_record_row(account_id=1, phone_number=1234567890, client_member_id=1234)
        ]
        self._common_flow(records_raw,[records_raw[0]])

    def test_bulk_upload_same_account_different_rest(self,_):
        records_raw = [
            self.create_record_row(account_id=1,phone_number=9087654321,client_member_id=1234),
            self.create_record_row(account_id=1, phone_number=1234567890, client_member_id=4321)
        ]
        self._common_flow(records_raw,records_raw)

    def test_bulk_upload_wrong_headers(self,_):
        records_raw = [self.create_record_row(i) for i in range(5)]
        headers_out_of_order = [self.VALID_HEADERS[1]] + [self.VALID_HEADERS[0]] + list(self.VALID_HEADERS[2:])
        print(f"headers_out_of_order: {headers_out_of_order}")
        self._common_flow(records_raw, headers=headers_out_of_order,expected_error_code=400)

    def test_bulk_upload_invalid_phone_number(self,_):
        records_raw = [self.create_record_row(phone_number=1234567)]
        self._common_flow(records_raw, [])






