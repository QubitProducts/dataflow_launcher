import logging
import time

SEPARATOR = '-'
CATCH_ALL_SUBSCRIPTION = 'default-subscription'


def get_pubsub_name(project_id, resource_type, name):
    return 'projects/{}/{}/{}'.format(project_id, resource_type, name)


def get_topic_name(project_id, topic):
    return get_pubsub_name(project_id, 'topics', topic)


def get_subscription_name(project_id, sub):
    return get_pubsub_name(project_id, 'subscriptions', sub)


def check_if_topic_exists(topic, existing_topics):
    return {'name': topic} in existing_topics


def get_list_from_key(key, dictionary):
    return dictionary.get(key, [])


def create_topic_if_not_exists(client, project_id, topic, existing_topics,
                               create_missing_topics):
    topic = get_topic_name(project_id, topic)
    if not check_if_topic_exists(topic, existing_topics):
        if not create_missing_topics:
            raise Exception("Topic {} does not exist".format(topic))
        # Topic does not exist, let's create it
        topic_ = client.projects().topics().create(
            name=topic, body={}).execute()
        if any([topic_ is None,
                'name' not in topic_,
                topic_['name'] != topic]):
            raise Exception(
                "Unknown error while creating topic [{}]".format(topic))
        logging.info('Created missing topic', topic_)


def create_subscription_if_not_exists(
        client, project_id, topic_name, sub_name,
        create_missing_subs):
    if not check_if_subscription_exists(
            client, project_id, topic_name, sub_name):
        if not create_missing_subs:
            raise Exception("Subscription {} does not exist".format(sub_name))
        create_subscription(client, project_id, topic_name, sub_name)


def check_if_subscription_exists(client, project_id, topic_name, sub_name):
    sub = get_subscription_name(project_id, sub_name)
    existing_subs = get_subscriptions_for_topic(client, project_id, topic_name)
    return sub in existing_subs


def get_subscriptions_for_topic(client, project_id, topic_name):
    topic = get_topic_name(project_id, topic_name)
    existing_subs = client.projects().topics().subscriptions().list(
        topic=topic).execute()
    existing_subs = get_list_from_key('subscriptions', existing_subs)
    return existing_subs


def check_if_topic_has_subscriptions(client, project_id, topic_name):
    existing_subs = get_subscriptions_for_topic(
        client, project_id, topic_name)
    return len(existing_subs) > 0


def create_subscription(client, project_id, topic_name, sub_name):
    topic = get_topic_name(project_id, topic_name)
    logging.info("Creating sub: %s for topic: %s", sub_name, topic_name)
    full_sub_name = get_subscription_name(project_id, sub_name)
    sub_ = client.projects().subscriptions().create(
        name=full_sub_name,
        body={'topic': topic}).execute()
    if any([sub_ is None, 'name' not in sub_, sub_['name'] != full_sub_name]):
        raise Exception(
            "Unknown error while creating subscription [{}]".format(
                full_sub_name))
    logging.info('Created subscription %s', sub_)


def setup_pubsub(project_id, topics, subs, create_missing_output_topics,
                 create_missing_subs, create_missing_input_topics):
    from oauth2client.client import GoogleCredentials
    from googleapiclient import discovery

    credentials = GoogleCredentials.get_application_default()
    client = discovery.build('pubsub', 'v1', credentials=credentials)
    existing_topics = client.projects().topics().list(
        project='projects/{}'.format(project_id)).execute()
    existing_topics = get_list_from_key('topics', existing_topics)

    if create_missing_input_topics:
        for sub in subs:
            create_topic_if_not_exists(
                client, project_id, sub[2], existing_topics, True)

    time.sleep(15)
    # wait for topics to be created

    for sub in subs:
        sub_name = sub[1]
        topic_name = sub[2]
        create_subscription_if_not_exists(
            client, project_id, topic_name, sub_name, create_missing_subs)

    for _, topic in topics:
        create_topic_if_not_exists(client, project_id, topic, existing_topics,
                                   create_missing_output_topics)
        if not check_if_topic_has_subscriptions(client, project_id, topic):
            create_subscription(client, project_id, topic, ''.join(
                [topic, SEPARATOR, CATCH_ALL_SUBSCRIPTION]))


# Subscription format: ${topic_name}_system
def get_formatted_subscription(topic_name, system):
    return '{}_{}'.format(topic_name, system)
