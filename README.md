# python-kafka-streams

[![Build Status](https://github.com/twosixlabs-dart/python-kafka-streams/workflows/Build/badge.svg)](https://github.com/twosixlabs-dart/python-kafka-streams/actions)

## What Is This?

This project is a part of a collection of Python examples for working with kafka Streams via the [`Faust`](https://faust.readthedocs.io) library. This particular project contains a simple stream processor implementation. The full suite of projects are the following:

- [Producer](https://github.com/twosixlabs-dart/python-kafka-producer)
- [Stream Processor](https://github.com/twosixlabs-dart/python-kafka-streams) (this project)
- [Consumer](https://github.com/twosixlabs-dart/python-kafka-consumer)
- [Environment](https://github.com/twosixlabs-dart/kafka-examples-docker)

The environment is detailed more [here](#Getting-Started).

The *stream processor* in this example is an agent that subscribes to the `stream.in` topic for events. When it receives an event, it updates the payload and forwards it along to the `stream.out` topic. That is it! This project is relatively simple, and so the structure of the project is simple and may not entirely reflect a complex application/use of `Faust`.

## Getting Started

Getting started with these examples requires a complete Kafka environment (with Zookeeper). The [Environment](https://github.com/twosixlabs-dart/kafka-examples-docker) project contains a docker-compose file for setting up everything. As this is a set of Python examples, just stand up the provided Python environment with:

```shell
docker-compose -f python.yml pull
docker-compose -f python.yml up -d
```

This will pull down the images needed and begin running everything. You can observe what is going on by looking at the logs for each of the three Python components (either one at a time or in multiple terminals):

```shell
docker logs -f kafka-examples-docker_stream-processor_1
docker logs -f kafka-examples-docker_producer
docker logs -f kafka-examples-docker_consumer
```

The stream-processor and producer will only have some startup and debug output, but the consumer will show messages being send through to the consumer's `stdout`, containing breadcrumbs from the producer, then the stream-processor, and finally the consumer itself.