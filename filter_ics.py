import boto3
import os
import requests
from icalendar import Calendar, Event

from copy import deepcopy

def filter_private_events(ics_data):
    cal = Calendar.from_ical(ics_data)
    filtered_cal = Calendar()

    # Copy properties from the original calendar to the filtered calendar
    for key in cal.keys():
        filtered_cal.add(key, cal.get(key))

    for event in cal.subcomponents:
        if event.name == "VEVENT":
            class_value = event.get("CLASS")
            private_event = class_value and class_value.upper() == "PRIVATE"

            # Log event information and whether it's marked as private
            print(f"Event UID: {event.get('UID')}")
            print(f"Event summary: {event.get('SUMMARY')}")
            print(f"Event description: {event.get('DESCRIPTION')}")
            print(f"Event class: {class_value}")
            print(f"Private event: {private_event}")

            # Clone the event component
            new_event = deepcopy(event)

            if private_event:
                # Replace summary and description for private events, remove location
                new_event["SUMMARY"] = os.getenv("PRIVATE_SUMMARY", "private event")
                new_event["DESCRIPTION"] = os.getenv("PRIVATE_DESC", "private event - details removed")
                new_event["LOCATION"] = ""

            # Add the (possibly modified) event to the filtered calendar
            filtered_cal.add_component(new_event)

    return filtered_cal.to_ical().decode("utf-8")


def lambda_handler(event, context):
    bucket_name = os.environ["BUCKET_NAME"]
    output_key = os.environ["OUTPUT_KEY"]
    source_url = os.environ["SOURCE_URL"]

    if not bucket_name:
        raise ValueError("Missing required environment variable: BUCKET_NAME")
    if not output_key:
        raise ValueError("Missing required environment variable: OUTPUT_KEY")
    if not source_url:
        raise ValueError("Missing required environment variable: SOURCE_URL")

    # Fetch iCalendar file via HTTP
    response = requests.get(source_url)
    ics_data = response.text

    # Filter private events
    filtered_data = filter_private_events(ics_data)

    # Write the filtered iCalendar data to S3
    s3 = boto3.client("s3")
    s3.put_object(Body=filtered_data, Bucket=bucket_name, Key=output_key)

