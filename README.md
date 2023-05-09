# ICSprivacy
Anonymize all events marked as "private" in an ICS feed and re-publish the resulting feed (AWS Lambda + S3)

## Prerequisites
- python
- URL of your calendar feed that needs to by anonymized (e.g. Google)
- AWS account with an S3 bucket set up

## Setup
- Setup virtual env: ```python3 -m venv venv```
- Activate venv: ```source venv/bin/activate'''
- Install requirements: ```pip install -r requirements.txt```
- Package up the code: ```zip -r lambda_package.zip filter_ics.py venv/lib/python*/site-packages/```
- Set up lambda function:
  - Create a new lambda function with the option "author from scratch". Choose a helpful name and select the python runtime that matches your local setup (```ls venv/lib/``` ;) ), create a new role and note the name of that role
  - upload lambda_package.zip 
  - under Configuration > Environment variables set the following fields to configure the script:
    - BUCKET_NAME: name of the target bucket where the filtered calendar feed should be uploaded
    - OUTPUT_KEY: filename of the resulting, filtered calendar feed
    - SOURCE_URL: URL of the input feed that needs to be anonymized
    - *(optional)* PRIVATE_SUMMARY: text that should replace the title of anonymized events (Default: "private event")
    - *(optional)* PRIVATE_DESC: text that should replace the description of anonymized events (Default: "private event - details removed")
  - add a trigger to run the script periodically (e.g. Amazon Eventbridge "rate 1h" to run in hourly)
  - in IAM modify that role to have access to your target S3 bucket 

## TODO
[x] customize label for private events
[x] anonymize location
[ ] private events should still be marked as PRIVATE
[x] error handling
