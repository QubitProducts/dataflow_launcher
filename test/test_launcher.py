import logging
from unittest import TestCase, main
from unittest.mock import patch

from dataflowlauncher import launcher
from dataflowlauncher.parsers.config_parsers import config_parser_main
from rootpath import get_absolute_path


class TestLauncher(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_no_unknown_arguments(self):
        formatted_param_list = launcher.get_formatted_launch_parameters(dict(), False, ['--evil-arg'])
        self.assertNotIn('--evil-arg', formatted_param_list)

    def test_unknown_arguments(self):
        env_list = launcher.get_formatted_launch_parameters(dict(), True, ['--evil-arg'])
        self.assertIn('--evil-arg', env_list)


    @patch("dataflowlauncher.parsers.config_parsers.required_config_parser.get_job_status", autospec=True)
    @patch("dataflowlauncher.parsers.config_parsers.required_config_parser.create_gcs_if_not_exists", autospec=True)
    def test_parameter_list_formatting(self, mock_dataflow_utils, mock_gcs_utils):
        mock_gcs_utils.return_value = None
        mock_dataflow_utils.return_value = None

        test_conf = config_parser_main.parse_config_file(get_absolute_path("_testing/test_conf.conf"))
        parameter_list = config_parser_main.get_jar_parameter_dict(test_conf)
        formatted_param_list = launcher.get_formatted_launch_parameters(parameter_list, False, [])
        self.assertCountEqual([
            '--project=test_project_id',
            '--stagingLocation=gs://test_project_id-temp',
            '--zone=test_zone',
            '--jobName=test',
            '--appName=test',
            '--numWorkers=1',
            '--workerMachineType=test_worker_type',
            '--defaultWorkerLogLevel=test_logLevel',
            '--streaming=true',
            '--runner=DataflowPipelineRunner',
            '--autoscalingAlgorithm=THROUGHPUT_BASED',
            '--maxNumWorkers=10',
            '--subscriptionName=projects/test_project_id/subscriptions/test_subscription_to_read_from_test',
            '--invalidatedTopicName=projects/test_project_id/topics/test_invalidated_topic_name',
            '--validatedTopicName=projects/test_project_id/topics/test_validated_topic_name',
            '--metricsReporterType=test_reporterType',
            '--metricsReporterPort=9125',
            '--metricsEnabled=true',
            '--update=false'
        ], formatted_param_list)


if __name__ == '__main__':
    main()
