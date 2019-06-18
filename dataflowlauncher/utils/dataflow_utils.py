"""Utility functions to talk to the dataflow service."""
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
import logging


def get_job_status(project_id, flow_name, region):
    """ Returns the status of a dataflow job given a job name."""
    credentials = GoogleCredentials.get_application_default()
    client = discovery.build('dataflow', 'v1b3', credentials=credentials)

    req = make_list_request(client, project_id, region)
    while req is not None:
        res = req.execute()
        try:
            for job in res['jobs']:
                if all(['name' in job, job['name'] == flow_name,
                        job['currentState'] == 'JOB_STATE_RUNNING']):
                    return job['id']
            req = make_next_request(client, region, req, res)
        except KeyError as e:
            logging.info("No jobs running in project.")
            break
    return None

def make_list_request(client, project_id, region):
    if region == None:
        return client.projects().jobs().list(projectId=project_id)
    else:
        return client.projects().locations().jobs().list(projectId=project_id, location=region)

def make_next_request(client, region, req, res):
    if (region == None):
        return client.projects().jobs().list_next(previous_request=req, previous_response=res)
    else:
        return client.projects().locations().jobs().list_next(previous_request=req, previous_response=res)
