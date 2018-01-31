import logging

from clint.textui import colored, puts

from dataflowlauncher.constants import (
    AUTOSCALING_TYPE,
    LOG_LEVEL,
    JOB_NAME,
    JOB_PROJECT_ID,
    JOB_ZONE,
    MAX_WORKER_COUNT,
    RUNNER,
    STAGING_STORAGE_BUCKET,
    STREAM_MODE,
    WORKER_COUNT,
    WORKER_TYPE,
    FLOW
)
from dataflowlauncher.parsers.config_parsers.base_config_parser import ConfigParser
from dataflowlauncher.utils.dataflow_utils import get_job_status
from dataflowlauncher.utils.gcs_utils import create_gcs_if_not_exists


class RequiredConfigParser(ConfigParser):
    def parse_config_file(self):
        configuration = dict()
        configuration[JOB_PROJECT_ID] = self.conf.get_string('required.project_id')
        configuration[JOB_NAME] = self.conf.get_string('required.name')
        configuration[JOB_ZONE] = self.conf.get_string('required.zone')
        configuration[WORKER_COUNT] = self.conf.get_string('required.num_workers', '1')
        configuration[WORKER_TYPE] = self.conf.get_string('required.worker_type', 'n1-standard-1')
        configuration[STREAM_MODE] = self.conf.get_bool('required.streaming', True)
        configuration[AUTOSCALING_TYPE] = self.conf.get('required.autoscaling_algorithm', "NONE")
        configuration[MAX_WORKER_COUNT] = self.conf.get('required.max_num_workers', None)
        configuration[RUNNER] = self.conf.get('required.runner', 'DataflowPipelineRunner')
        configuration[STAGING_STORAGE_BUCKET] = self.conf.get('required.staging_storage_bucket', None)
        configuration[LOG_LEVEL] = self.conf.get('required.log_level', 'INFO')

        return configuration

    def get_jar_params_from_conf(self, config):
        variables = {
            "project": config[JOB_PROJECT_ID],
            "jobName": config[JOB_NAME],
            "appName": config[JOB_NAME],
            "zone": config[JOB_ZONE],
            "numWorkers": config[WORKER_COUNT],
            "workerMachineType": config[WORKER_TYPE],
            "defaultWorkerLogLevel": config[LOG_LEVEL],
            "streaming": str(config[STREAM_MODE]).lower(),
            "runner": config[RUNNER]
        }
        variables.update(self.add_max_workers_from_autoscaling_type(config))
        variables.update(self.add_update_flag_to_config(config))
        variables.update(self.add_staging_storage_bucket(config))

        return variables

    @staticmethod
    def add_max_workers_from_autoscaling_type(config):
        result = dict()
        result["autoscalingAlgorithm"] = config[AUTOSCALING_TYPE]
        if config[AUTOSCALING_TYPE] == "THROUGHPUT_BASED":
            if config[MAX_WORKER_COUNT] is not None:
                result["maxNumWorkers"] = config[MAX_WORKER_COUNT]
        return result

    @staticmethod
    def add_update_flag_to_config(config):
        result = dict()
        is_update = 'false'
        job_running = get_job_status(config[JOB_PROJECT_ID], config[JOB_NAME], config[FLOW].get('region'))
        if job_running:
            logging.info("Located currently running job with ID: %s",
                         job_running)
            puts(colored.red('This command will update currently running job: %s' % job_running))
            is_update = 'true'
        else:
            logging.info("No currently running job with name: %s", config[JOB_NAME])

        result["update"] = is_update
        return result

    @staticmethod
    def add_staging_storage_bucket(config):
        result = dict()
        if config[STAGING_STORAGE_BUCKET] is None:
            staging_bucket_name = '%s-temp' % config[JOB_PROJECT_ID]
            create_gcs_if_not_exists(staging_bucket_name, config[JOB_ZONE], config[JOB_PROJECT_ID])
            result["stagingLocation"] = 'gs://%s/dataflow_launcher' % staging_bucket_name
        else:
            result["stagingLocation"] = config[STAGING_STORAGE_BUCKET]

        return result
