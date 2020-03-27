import asynctest
import pytest
from pystreams.app import app
from pystreams.messages.stream_message import StreamMessage
from pystreams.streams.agents import stream_in, stream_out_topic


@pytest.fixture()
def basic_stream_processor(event_loop):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    app.finalize()
    app.conf.store = 'memory://'
    app.flow_control.resume()
    return app


@pytest.fixture()
def sample_messages(event_loop):
    sample_message_1 = StreamMessage(id='test1', breadcrumbs=[])
    sample_message_2 = StreamMessage(id='test1', breadcrumbs=['python-kafka-streams'])
    return {'empty': sample_message_1, 'full': sample_message_2}


@pytest.mark.asyncio()
@pytest.mark.usefixtures('basic_stream_processor', 'sample_messages')
async def test_event_forwarding(mocker, basic_stream_processor, sample_messages):
    with asynctest.mock.patch.object(stream_out_topic, 'send'):
        async with basic_stream_processor.agents['pystreams.streams.agents.stream_in'].test_context() as agent:
            await agent.put(sample_messages['empty'])
            stream_out_topic.send.assert_called_with(value=sample_messages['full'])


@pytest.mark.asyncio()
@pytest.mark.usefixtures('basic_stream_processor', 'sample_messages')
async def test_event_update(mocker, basic_stream_processor, sample_messages):
    with asynctest.mock.patch.object(stream_out_topic, 'send'):
        async with basic_stream_processor.agents['pystreams.streams.agents.stream_in'].test_context() as agent:
            event = await agent.put(sample_messages['empty'])
            assert agent.results[event.message.offset] == sample_messages['full']
