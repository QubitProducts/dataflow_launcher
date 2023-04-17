"""Utility functions for Google Cloud Storage."""
import json
import logging

from googleapiclient import discovery

from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials


def create_gcs_if_not_exists(bucket_name, region, project_id):
    """ Creates a GCS bucket if it does not exist."""
    credentials = GoogleCredentials.get_application_default()
    client = discovery.build('storage', 'v1', credentials=credentials, cache_discovery=False)
    try:
        client.buckets().get(bucket=bucket_name).execute()
    except HttpError as exception:
        logging.info(exception)
        req = client.buckets().insert(
            project=project_id,
            body={'name': bucket_name, 'region': region})
        resp = req.execute()
        logging.debug(json.dumps(resp, indent=2))
