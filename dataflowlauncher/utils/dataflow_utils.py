"""Utility functions to talk to the dataflow service."""
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery


def get_job_status(project_id, flow_name):
    """ Returns the status of a dataflow job given a job name."""
    credentials = GoogleCredentials.get_application_default()
    client = discovery.build('dataflow', 'v1b3', credentials=credentials)

    req = client.projects().jobs().list(projectId=project_id)
    while req is not None:
        res = req.execute()
        for job in res['jobs']:
            if all(['name' in job, job['name'] == flow_name,
                    job['currentState'] == 'JOB_STATE_RUNNING']):
                return job['id']
        req = client.projects().jobs().list_next(previous_request=req, previous_response=res)
    return None
