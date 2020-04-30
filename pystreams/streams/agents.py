from faust import StreamT
from pystreams import config


def create_streams(app):
    # create topics
    stream_in_topic = app.topic(config['topic']['from'], key_type=str, value_type=str)
    stream_out_topic = app.topic(config['topic']['to'], key_type=str, value_type=str)

    # create an agent subscribed to the stream.in topic. this function receives
    # events, updates them, and then forwards them to the stream.out topic
    @app.agent(stream_in_topic)
    async def stream_in(stream: StreamT):
        """Update and forward events to the stream_out_topic topic"""
        auto_commit = config['app'].get('enable_auto_commit', False)
        events = stream.events() if auto_commit else stream.noack().events()
        async for event in events:
            event.value['value'].append('python-kafka-streams')
            await stream_out_topic.send(key=event.key, value=event.value)
            yield event

    return stream_in_topic, stream_out_topic
