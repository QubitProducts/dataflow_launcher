# Dataflow Launcher #

Seamlessly launch dataflow jobs without worrying about paths, options, updates, and pubsub creation.

### Installation? ###
`pip install git+ssh://git@github.com/QubitProducts/dataflow_launcher.git`

### Requirements ###
It will use your locally stored `gcloud` credentials to launch the jobs.
You must ensure that the account you have set up has the correct rights to the project you're attempting to deploy to.

### How to run it? ###
`python3 -m dataflowlauncher.launcher`

Make sure you have `flow.conf` in the current directory. In addition, the script assumes that the current directory also contains the git root.

## PEX Distribution

Make sure you have `virtualenv` installed.

**Tests:**
`make test` or `tox`

**Package PEX:**
`make build`

**Executing PEX**
`./target/dataflow_launcher.pex`

**Installing from source:**
`pip install .`

### Usage
**Flags:**

`-f` or `--file`: Configuration file name. Default: `flow.conf`

`-c` or `--create_missing_output_topics`: Create missing output pubsub topics Default: `false`

`-i` or `--create_missing_input_topics`: Create missing input pubsub topics Default: `false`

`-u` or `--create_missing_subscriptions`: Create missing input pubsub subscriptions Default: `false`

`-j` or `--jar_path`: Relative path to the JAR directory. Default: target

`--jar_file`: Path to the JAR file. Overrides -j. Default: NONE

`--ignore_git`: Don't check that the git branch is clean

`-b` or `--bypass_prompt`: Skip the enter key press required before launching

`--override_arguments`: Pass a list of arguments to the underlying command, overriding any set via the config file, specified as a space-separated list of \<key>=\<value> pairs


**SDK/Runner Support**
- *Dataflow SDK 1.9.1 and lower* - no configuration changes needed
- *BEAM 2.0.0 and newer* - need to specify correct runner

### Program flow structure ###

- Read the configuration file using the registered configuration readers
- Update the read configuration dictionary with any overrides from the registered cli argument readers
- Run any setup/preprocessing commands required by the cli arguments
- Transform configuration dictionary into a parameter dictionary using the registered configuration readers
- Update the parameter dictionary with any overrides from the registered cli argument readers
- Transform the parameter dictionary into a list of formatted parameters
- Figure out JAR path if not specified
- Launch flow with the parameter list

**Concepts:**

- **configuration** - values read from the configuration file or values that were added due to cli arguments
- **parameter** - values to be passed as to the underlying `java -jar` call
- **configuration reader** - A class that extends `ConfigParser` and knows how to pick up values from the `.conf` file.
It should also be able to transform the configuration into parameters for the launch command.
It gets registered in `config_parser_main`.
- **cli reader** - A class that extends `CliParser` and registers cli arguments to the parser.
Has options to update configuration or parameters and run additional setup steps.
It gets registered in `cli_parser_main`.

### Configuration ###

All configuration information needs to be present in `flow.conf`

### Sample flow.conf ###
```
required {
  project_id: "test_project_id"
  name: "test"
  zone: "test_zone"
  num_workers: 1
  autoscaling_algorithm: "THROUGHPUT_BASED"
  max_num_workers: 10
  worker_type: "test_worker_type"
  runner: "PipelineRunner"
  staging_storage_bucket: "gs://somebucket/directory"
  log_level: "test_logLevel"
}

pom {
  name: "test_pom.xml"
  generated_jar_name: "{artifact}-{version}-dist.jar"
}

pubsub {
  read = {
    "subscriptionName": "test_subscription_prefix"
  }

  read_verbatim = {
    "verbatimSubscriptionName": "some_test_verbatim_subscription"
  }

  write = {
    "validatedTopicName": "test_validated_topic_name"
    "invalidatedTopicName": "test_invalidated_topic_name"
  }
}

flow {
  metricsEnabled: "true"
  metricsReporterPort: 9125
  metricsReporterType: "test_reporterType"
}
```

### Required Configuration ###
The required configuration handles Dataflow related options.
We've added some default values to some of the options. The options are:
```
required {
  project_id: "test_project_id"
  name: "test"
  zone: "test_zone"
  num_workers: 1
  autoscaling_algorithm: "THROUGHPUT_BASED"
  max_num_workers: 10
  worker_type: "test_worker_type"
  runner: "PipelineRunner"
  staging_storage_bucket: "gs://somebucket/directory"
  log_level: "test_logLevel"
}
```

- `required.project_id`: Id of the project the flow will run in.
- `required.name`: The name of the dataflow job.
- `required.zone`: The zone the flow will run in.
- `required.num_workers`: The number of dataflow workers. Default: `1`
- `required.autoscaling_algorithm`: The type of autoscaling algorithm to use. Current options are `THROUGHPUT_BASED` and `NONE`. Default: `NONE`
- `required.max_num_workers`: The maximum number of workers the flow will scale up to.
- `required.streaming`: The mode of dataflow running: true - streaming, false - batch. Default: `true`
- `required.worker_type`: The type of dataflow workers. Default: `n1-standard-1`
- `required.runner`: The runner the job will work with. This will tie into the Dataflow/Beam version you're using. Default: `DataflowPipelineRunner`
- `required.storage_staging_bucket`: The bucket where to store and run the jar from. Will create one based on project id if unspecified.
- `required.log_level`: Log level for the job. Default: `INFO`

### Pom Configuration ##
```
 pom {
    name: "test_pom.xml"
    pom.generated_jar_name: "{artifact}-{version}-test.jar"
 }
```

- `pom.name`: Path to POM file. Default: `pom.xml`
- `pom.generated_jar_name`: The name of the generated jar file. Default: `{artifact}-{version}.jar`. `{artifact}` and `{version}` will be replaced by the artifact-id and version as defined in the pom file

The launcher will attempt to figure out the artifact to deploy if the configuration for the jar was not passed in the arguments.
It's currently set up to work with Java projects that have been build with `maven`.
It will look in the `pom.xml` to get the name of the jar and will assume it lives in `target`.

### Pubsub Configuration & CLI ###
**Configuration**
We've set a convention for the subscription names, to be able to create input topics if they do not exist.
Check the following example:
```
required {
  project_id: "testProjectId"
  name: "flowName"
}

pubsub {
  read = {
    "subscription": "test_subscription_prefix"
  }
}
```
where `subscription` is the subscription option name and `test_subscription_prefix` is the topic name.
The launcher will translate this into the parameter `--subscription=projects/testProjectId/subscriptions/test_subscription_prefix_flowName`

If you have an existing subscription that you would like to make use of, use `read_verbatim` and check the same example:
```
required {
  project_id: "testProjectId"
  name: "flowName"
}

pubsub {
  read_verbatim = {
    "subscription": "some_subscription_name"
  }
}
```
The command you'd get would be: `--subscription=projects/testProjectId/subscriptions/some_subscription_name`

The `read_verbatim` option also allows reading of subscriptions from external projects, by setting the `project_id` field, eg:
```
required {
  project_id: "testProjectId"
  name: "flowName"
}

pubsub {
  read_verbatim = {
    "project_id": "external_project_id"
    "subscription": "some_subscription_name"
  }
}
```
The command you'd get from this configuration would be `--subscription=projects/external_project_id/subscriptions/some_subscription_name`

In contrast, topics under `pubsub.write` only need to contain the topic name. For instance,
```
required {
  project_id: "testProjectId"
  name: "flowName"
}

pubsub {
  write = {
    "topic": "some_test_topic_name"
  }
}
```

The command you'd get would be `--topic=projects/testProjectId/topics/some_test_topic_name`.

**Commands Notes**
- `--create_missing_output_topics`
    This will also create a default subscription onto the topic created. W/o any subscriptions the data is not persisted.
- `-i` or `--create_missing_input_topics`
    In order for this to work properly, the naming convention described above needs to be upheld.
- `--override_arguments` This command takes a list of `<key>=<value>` pairs, and passes them directly to the underlying dataflow launch command. These will override any corresponding values set in the config file. For example:

### Utility CLI ###
```
required {
  project_id: "testProjectId"
  name: "flowName"
}

pubsub {
  read_verbatim = {
    "subscription": "some_subscription_name"
  }
}
```

- Running with the cli option `--override_arguments subscription=different_subscription` will result in the dataflow being launched with `--subscription=different_subscription` instead of `--subscription=projects/testProjectId/subscriptions/some_test_topic_name`. 

**Note** that there can be a difference between the field name set in the config file, and that which is sent to the dataflow launch command, eg: `num_workers` maps to `numWorkers`, so to override this value you would use `--override_arguments numWorkers=4` for example.
