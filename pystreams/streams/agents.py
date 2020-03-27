from faust.streams import Stream
from pystreams.app import app
from pystreams.messages.stream_message import StreamMessage


stream_in_topic = app.topic('stream.in', value_type=StreamMessage)
stream_out_topic = app.topic('stream.out', value_type=StreamMessage)


@app.agent(stream_in_topic)
async def stream_in(stream : Stream):
    """Update and forward events to the stream_out agent"""
    async for event in stream:
        event.breadcrumbs.append('python-kafka-streams')
        await stream_out_topic.send(value=event)
        yield event
