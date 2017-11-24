from unittest import TestCase, main

from dataflowlauncher.utils.pub_sub_utils import (
    check_if_topic_exists,
    get_list_from_key,
    get_topic_name,
    get_subscription_name,
    get_subscriptions_for_topic,
    check_if_topic_has_subscriptions)


class MockExec(object):

    def __init__(self, ret):
        self._ret = ret

    def execute(self):
        return self._ret


class MockSub(object):

    def __init__(self, key, val):
        self._topics = {key: MockExec(val)}
        self._default = MockExec({})

    def list(self, topic):
        topic = topic.split('/')[3]
        return self._topics.get(topic, self._default)


class MockTopic(object):

    def __init__(self, key, val):
        self._key = key
        self._val = val

    def subscriptions(self):
        return MockSub(self._key, self._val)


class MockProject(object):

    def __init__(self, key, val):
        self._key = key
        self._val = val

    def topics(self):
        return MockTopic(self._key, self._val)


class MockPubsubClient(object):

    def __init__(self, key, val):
        self._key = key
        self._val = val

    def projects(self):
        return MockProject(self._key, self._val)


class TestPubsubUtils(TestCase):

    def test_topic_exists_fail_empty(self):
        self.assertEqual(
            check_if_topic_exists('mytopic', []), False)

    def test_topic_exists_fail_missing(self):
        self.assertEqual(
            check_if_topic_exists('mytopic',
                                  [{'name': 'randomtopic'}]),
            False)

    def test_topic_exists_pass(self):
        self.assertEqual(
            check_if_topic_exists('mytopic', [{'name': 'mytopic'}]), True)

    def test_list_key_fail(self):
        self.assertEqual(get_list_from_key('foo', {'fooz': ['baz']}), [])

    def test_list_key_pass(self):
        self.assertEqual(get_list_from_key('foo', {'foo': ['baz']}), ['baz'])

    def test_get_topic_fqn(self):
        self.assertEqual(get_topic_name('myproject', 'mytopic'),
                         'projects/myproject/topics/mytopic')

    def test_get_sub_fqn(self):
        self.assertEqual(get_subscription_name('myproject', 'mysub'),
                         'projects/myproject/subscriptions/mysub')

    def test_get_subs_for_topic_found(self):
        subs = ['mysub1', 'mysub2']
        topic = 'mytopic'
        client = MockPubsubClient(topic, {'subscriptions': subs})
        self.assertEqual(
            get_subscriptions_for_topic(client, 'myproject', topic), subs)

    def test_get_subs_for_topic_missing(self):
        subs = ['mysub1', 'mysub2']
        topic = 'mytopic'
        client = MockPubsubClient(topic, {'subscriptions': subs})
        self.assertEqual(
            get_subscriptions_for_topic(client, 'myproject', 'foo'), [])

    def test_check_if_topic_has_subscriptions_found(self):
        subs = ['mysub1', 'mysub2']
        topic = 'mytopic'
        client = MockPubsubClient(topic, {'subscriptions': subs})
        self.assertEqual(
            check_if_topic_has_subscriptions(client, 'myproject', topic),
            True)

    def test_check_if_topic_has_subscriptions_missing(self):
        subs = ['mysub1', 'mysub2']
        topic = 'mytopic'
        client = MockPubsubClient(topic, {'subscriptions': subs})
        self.assertEqual(
            check_if_topic_has_subscriptions(client, 'myproject', 'foo'),
            False)


if __name__ == '__main__':
    main()
