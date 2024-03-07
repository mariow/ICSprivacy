# ICSprivacy

Yet another script to filter an ICS feed and remove all details from events marked as "private". I know, there's lots of existing scripts but I found none that really fixed my small issue (the usual excuse).

The script is designed to run as an AWS lambda function that regularly pulls a calendar feed via HTTP (e.g. from Google calendar), removes all details from events marked as private ("CLASS:PRIVATE") and republishes the resulting feed to an S3 bucket. Entries older than 365 days are removed.

## Prerequisites
- python
- URL of your calendar feed that needs to by anonymized (e.g. Google)
- AWS account with an S3 bucket set up

## Setup
- Setup virtual env: ```python3 -m venv .```
- Activate venv: ```source bin/activate'''
- Install requirements: ```pip install -r requirements.txt```
- Package up the code:
  - ```cd lib/python*/site-packages/```
  - ```zip -r9 ../../../lambda_package.zip .```
  - ```cd ../../../```
  - ```zip -g lambda_package.zip filter_ics.py```
- Set up lambda function:
  - Create a new lambda function with the option "author from scratch". Choose a helpful name and select the python runtime that matches your local setup (```ls lib/``` ;), create a new role and note the name of that role
  - upload lambda_package.zip 
  - under General configuration set the timeout to a much higher value than the default 3s; I use 2 minutes which is usually way too much
  - under Configuration > Environment variables set the following fields to configure the script:
    - BUCKET_NAME: name of the target bucket where the filtered calendar feed should be uploaded
    - OUTPUT_KEY: filename of the resulting, filtered calendar feed
    - SOURCE_URL: URL of the input feed that needs to be anonymized
    - *(optional)* PRIVATE_SUMMARY: text that should replace the title of anonymized events (Default: "private event")
    - *(optional)* PRIVATE_DESC: text that should replace the description of anonymized events (Default: "private event - details removed")
  - add a trigger to run the script periodically (e.g. Amazon Eventbridge "rate 1h" to run in hourly)
  - in IAM modify that role to have access to your target S3 bucket 

