from faust import StreamT
from pystreams.app import app
from pystreams.messages.stream_message import StreamMessage


# create topics
stream_in_topic = app.topic('stream.in', value_type=StreamMessage)
stream_out_topic = app.topic('stream.out', value_type=StreamMessage)


# create an agent subscribed to the stream.in topic. this function receives
# events, updates them, and then forwards them to the stream.out topic
@app.agent(stream_in_topic)
async def stream_in(stream: StreamT):
    """Update and forward events to the stream_out_topic topic"""
    async for event in stream:
        event.breadcrumbs.append('python-kafka-streams')
        await stream_out_topic.send(value=event)
        yield event
