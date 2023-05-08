# ICSprivacy
Anonymize all events marked as "private" in an ICS feed and re-publish the resulting feed (AWS Lambda + S3)

## Setup
...venv...lambda...permissions...trigger
python3 -m venv venv
source venv/bin/activate
git@github.com:mariow/ICSprivacy.git

update code:
zip -g lambda_package.zip filter_ics.py
cp lambda_package.zip /mnt/c/Users/mario/Downloads/

## TODO
- customize label for private events
- anonymize location
- private events should still be marked as PRIVATE
- error handling
