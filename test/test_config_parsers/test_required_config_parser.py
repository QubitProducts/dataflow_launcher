import logging
from rootpath import get_absolute_path
from unittest import TestCase, main
from unittest.mock import patch

from dataflowlauncher.parsers.config_parsers.required_config_parser import (
    AUTOSCALING_TYPE,
    LOG_LEVEL,
    JOB_NAME,
    JOB_PROJECT_ID,
    JOB_ZONE,
    MAX_WORKER_COUNT,
    RUNNER,
    STREAM_MODE,
    WORKER_COUNT,
    WORKER_TYPE
)
from dataflowlauncher.custom_exceptions import ConfigFileNotFoundException
from dataflowlauncher.parsers.config_parsers.required_config_parser import \
    RequiredConfigParser


class TestRequiredConfigParser(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.parser = RequiredConfigParser()
        self.test_file_name = get_absolute_path("_testing/test_conf.conf")

    def test_file_exists(self):
        self.parser.get_config_parameters(self.test_file_name)

    def test_file_exists_when_no_file(self):
        with self.assertRaises(ConfigFileNotFoundException):
            self.parser.get_config_parameters("BOGUS")

    def test_parse_config_file(self):
        parsed_config = self.parser.get_config_parameters(self.test_file_name)
        reference_config = {
            JOB_NAME: "test",
            WORKER_COUNT: "1",
            JOB_ZONE: "test_zone",
            LOG_LEVEL: "test_logLevel",
            AUTOSCALING_TYPE: "THROUGHPUT_BASED",
            MAX_WORKER_COUNT: 10,
            WORKER_TYPE: "test_worker_type",
            JOB_PROJECT_ID: "test_project_id",
            RUNNER: "TestRunner",
            STREAM_MODE: True,
        }
        self.assertDictEqual(parsed_config, reference_config)

    @patch("dataflowlauncher.parsers.config_parsers." \
           "required_config_parser.get_job_status", autospec=True)
    @patch("dataflowlauncher.parsers.config_parsers." \
           "required_config_parser.create_gcs_if_not_exists", autospec=True)
    def test_get_jar_params_from_conf(self, mock_job_status, mock_gcs_call):
        mock_gcs_call.return_value = None
        mock_job_status.return_value = True
        parsed_config = self.parser.get_config_parameters(self.test_file_name)
        jar_args = self.parser.get_jar_params_from_conf(parsed_config)
        reference_args = dict(
            appName="test",
            autoscalingAlgorithm="THROUGHPUT_BASED",
            defaultWorkerLogLevel="test_logLevel",
            jobName="test",
            maxNumWorkers=10,
            numWorkers="1",
            project="test_project_id",
            runner="TestRunner",
            stagingLocation="gs://test_project_id-temp",
            streaming="true",
            update="false",
            workerMachineType="test_worker_type",
            zone="test_zone",
        )
        self.assertDictEqual(reference_args, jar_args)

    def test_add_max_workers_from_autscaling_type(self):
        sample_config = dict(
            AUTOSCALING_TYPE="THROUGHPUT_BASED",
            MAX_WORKER_COUNT=10,
        )
        result = self.parser.add_max_workers_from_autoscaling_type(
            sample_config)
        self.assertEqual(sample_config[AUTOSCALING_TYPE],
                         result.get("autoscalingAlgorithm"))
        self.assertEqual(sample_config[MAX_WORKER_COUNT],
                         result.get("maxNumWorkers"))

    def test_add_max_workers_from_autscaling_type_alternative_alg_name(self):
        sample_config = dict(
            AUTOSCALING_TYPE="BLA",
        )
        result = self.parser.add_max_workers_from_autoscaling_type(
            sample_config)
        self.assertEqual(sample_config[AUTOSCALING_TYPE],
                         result["autoscalingAlgorithm"])
        self.assertNotIn("maxNumWorkers", result)

    def test_add_max_workers_from_autscaling_type_same_name_none_workers(
            self):
        sample_config = dict(
            AUTOSCALING_TYPE="THROUGHPUT_BASED",
            MAX_WORKER_COUNT=None
        )
        result = self.parser.add_max_workers_from_autoscaling_type(
            sample_config)
        self.assertEqual(sample_config[AUTOSCALING_TYPE],
                         result["autoscalingAlgorithm"])
        self.assertNotIn("maxNumWorkers", result)

    @patch("dataflowlauncher.parsers.config_parsers." \
           "required_config_parser.get_job_status", autospec=True)
    def test_add_update_flag_to_config_true(self, mock_job_status):
        mock_job_status.return_value = True
        sample_config = dict(JOB_PROJECT_ID="test_job", JOB_NAME="test_name")
        result = self.parser.add_update_flag_to_config(sample_config)
        self.assertEqual("true", result["update"])


    @patch("dataflowlauncher.parsers.config_parsers." \
           "required_config_parser.get_job_status", autospec=True)
    def test_add_update_flag_to_config_false(self, mock_job_status):
        mock_job_status.return_value = False
        sample_config = dict(JOB_PROJECT_ID="test_job", JOB_NAME="test_name")
        result = self.parser.add_update_flag_to_config(sample_config)
        self.assertEqual("false", result["update"])

    @patch("dataflowlauncher.parsers.config_parsers." \
           "required_config_parser.create_gcs_if_not_exists", autospec=True)
    def test_add_staging_storage_bucket(self, mock_gcs_call):
        mock_gcs_call.return_value = None
        sample_config = dict(JOB_PROJECT_ID="test", JOB_ZONE="test_zone")
        reference_result = "gs://%s-temp" % sample_config[JOB_PROJECT_ID]
        result = self.parser.add_staging_storage_bucket(sample_config)
        self.assertEqual(reference_result, result["stagingLocation"])


if __name__ == '__main__':
    main()
