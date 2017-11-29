import logging
from unittest import TestCase, main

from dataflowlauncher.parsers.config_parsers.pubsub_config_parser import (
    JOB_PROJECT_ID,
    JOB_NAME,
    PUBSUB_WRITE,
    PUBSUB_READ,
    PUBSUB_READ_VERBATIM,
    PubSubConfigParser
)
from rootpath import get_absolute_path


class TestPubSubConfigParser(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.parser = PubSubConfigParser()
        self.test_file_name = get_absolute_path("_testing/test_conf.conf")
        self.maxDiff = None

    def test_parse_config_file(self):
        parsed_config = self.parser.get_config_parameters(self.test_file_name)
        reference_config = {
            PUBSUB_READ: {
                "subscriptionName": "test_subscription_to_read_from"},
            PUBSUB_WRITE: {
                "invalidatedTopicName": "test_invalidated_topic_name",
                "validatedTopicName": "test_validated_topic_name"},
            PUBSUB_READ_VERBATIM: {},
        }
        self.assertDictEqual(parsed_config, reference_config)

    def test_get_jar_params_from_conf(self):
        sample_config = {
            PUBSUB_WRITE: {
                "invalidatedTopicName": "test_invalidated_topic_name",
                "validatedTopicName": "test_validated_topic_name"},
            PUBSUB_READ: {
                "subscriptionName": "test_subscription_to_read_from"},
            PUBSUB_READ_VERBATIM: {
                "subscriptionNameVerbatim": "test_subscription_to_read_from"},
            JOB_PROJECT_ID: "test_id",
            JOB_NAME: "test_name"
        }
        jar_args = self.parser.get_jar_params_from_conf(sample_config)
        reference_args = {
            "validatedTopicName":
                "projects/test_id/topics/test_validated_topic_name",
            "invalidatedTopicName":
                "projects/test_id/topics/test_invalidated_topic_name",
            "subscriptionName": "projects/test_id/subscriptions/"\
                "test_subscription_to_read_from_test_name",
            "subscriptionNameVerbatim": "projects/test_id/subscriptions/"\
                "test_subscription_to_read_from",
        }
        self.assertDictEqual(reference_args, jar_args)

    def test_add_topic_variables(self):
        sample_config = {
            PUBSUB_WRITE: {
                "invalidatedTopicName": "test_invalidated_topic_name",
                "validatedTopicName": "test_validated_topic_name"},
            JOB_PROJECT_ID: "test_id"
        }
        reference_result = {
            "validatedTopicName":
                "projects/test_id/topics/test_validated_topic_name",
            "invalidatedTopicName":
                "projects/test_id/topics/test_invalidated_topic_name"
        }
        result = self.parser.add_topic_variables(sample_config)
        self.assertDictEqual(reference_result, result)

    def test_add_subscription_variables(self):
        sample_config = {
            PUBSUB_READ: {
                "subscriptionName": "test_subscription_to_read_from"},
            JOB_PROJECT_ID: "test_id",
            JOB_NAME: "test_name"
        }
        reference_result = {
            "subscriptionName":
                "projects/test_id/subscriptions/"\
                "test_subscription_to_read_from_test_name",
            }
        result = self.parser.add_subscription_variables(sample_config)
        self.assertDictEqual(reference_result, result)

    def test_add_subscription_verbatim(self):
        sample_config = {
            PUBSUB_READ_VERBATIM: {
                "subscriptionName": "test_subscription_to_read_from"},
            JOB_PROJECT_ID: "test_id",
            JOB_NAME: "test_name"
        }
        reference_result = {
            "subscriptionName":
                "projects/test_id/subscriptions/"\
                "test_subscription_to_read_from",
            }
        result = self.parser.add_subscription_verbatim(sample_config)
        self.assertDictEqual(reference_result, result)

    def test_add_external_project_subscription_verbatim(self):
        sample_config = {
            PUBSUB_READ_VERBATIM: {
                "project_id": "external_project",
                "subscriptionName": "test_subscription_to_read_from"},
            JOB_PROJECT_ID: "test_id",
            JOB_NAME: "test_name"
        }
        reference_result = {
            "subscriptionName":
                "projects/external_project/subscriptions/" \
                "test_subscription_to_read_from",
        }
        result = self.parser.add_subscription_verbatim(sample_config)
        self.assertDictEqual(reference_result, result)


if __name__ == '__main__':
    main()
