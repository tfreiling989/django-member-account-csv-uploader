# Member Account - Bulk Upload (CSV file) 

## How to Run The Application (Development)
1) Install Python (tested with 3.10.4)
2) Create and activate virtual environment. See https://docs.python.org/3/library/venv.html#module-venv
   (`python -m venv env`)
3) Install requirements (`pip install -r requirements.txt`)
4) Run sql migration (sqlite): `python manage.py migrate`
5) In venv, in 2 different terminals:
   1) Start webserver: `python manage.py runserver`
   2) Start background tasks: `python manage.py process_tasks`

## Example Apis
### Member Account View Set
You can navigate to `http://localhost:8000/members/` to access this ViewSet
#### Get a member for a given Account ID
`http://localhost:8000/members/?account_id=1`

#### Get a member by their ID
`http://localhost:8000/members/1/`

#### Get a member by their Phone Number
`http://localhost:8000/members/?phone_number=1284628753`

#### Get a member by their Client Member ID
`http://localhost:8000/members/?client_member_id=9436555`

#### Create a new Member
`curl -X POST http://localhost:8000/members/ -H 'Content-Type: application/json' -d '{"first_name":"Thomas","last_name":"Freiling","phone_number":"1234567890","client_member_id":"123","account_id":"10"}'`

### Batch Create Member Accounts (csv file upload)
Assuming `member_data.csv` is in current directory:
`curl -X POST http://localhost:8000/members/importcsv -F file=@member_data.csv`

## Design Notes
1) Note, this is my first Django application, so I'm sure there are quirks.
2) It may be desirable to have different records/tables for members and member accounts,
   depending on business requirements. There was no such requirement mentioned, so kept it simple as one table.
3) There is no auth setup. This would obviously need to be present in a real production system.
4) There isn't good documentation around the batch upload api. Could use something like swagger
5) For production, should use a more suitable db (i.e. postgres), this solution uses sqlite.
6) There is currently no reporting on rows that were failed to get created because:
   1) It was not part of the requirements
   2) It added more complexity. I used bulk_create with ignore_conflicts set for efficiency.
      If desired, could find records that were not created using something like an indexed created_at field.
   3) Did not want to log PII to logs and no other reporting structure was requested
   4) Its possible there could already be a sufficient reporting structure (i.e. using datawarehouse)
7) If I were to re-design this data upload mechanism:
   1) At the least, I would limit input file size, requiring clients to split up large files.
   2) I would not use background tasks, and instead have the client be responsible for batching and parsing the files.
   3) The BE batch upload api would accept json, and respond with which records failed and why, limiting the amount of records the api can support
   4) The client could be a jenkins job or similar, which could:
      1) run on a cron schedule (or manually triggered), ran during off hours
      2) grab newly uploaded files from S3 (i.e. in an input/ directory)
      3) batch and parse the files, converting them to json and calling BE api to upload each batch one at a time.
      4) accumulate any failed records and put them into S3 (i.e. in an error/ directory) 
      5) for transient errors, have retry mechanisms built in and if that fails retry the file the next time the service runs (can set retry limits as well using s3 file metadata)
      6) For data issues, can email people responsible for the data.
      7) For BE issues, can email appropriate BE engineering team (our team)
   5) Pros:
      1) Clear and convenient reporting/accumulation of errors
      2) Minimal interference with live system / scalable
   6) Cons:
      1) Slightly more bandwidth usage since there are multiple requests (however this traffic is spreadout)
      2) Requires S3 and jenkins (or similar (i.e. dedicated microservice))