import os
os.environ['PROGRAM_ARGS'] = 'test.json'
import asynctest
import pytest
import faust
from pystreams.app import create_app


app, topics = create_app()


@pytest.fixture()
def basic_stream_processor(event_loop):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    app.finalize()
    app.conf.store = 'memory://'
    app.flow_control.resume()
    return app


@pytest.fixture()
def sample_message(event_loop):
    return {"key": "test1", "value": []}


@pytest.mark.asyncio()
@pytest.mark.usefixtures('basic_stream_processor', 'sample_message')
async def test_event_forwarding(mocker, basic_stream_processor, sample_message):
    with asynctest.mock.patch.object(topics[1], 'send'):
        async with basic_stream_processor.agents['pystreams.streams.agents.stream_in'].test_context() as agent:
            await agent.put(key='sample', value=sample_message)
            topics[1].send.assert_called_with(key='sample', value=sample_message)


@pytest.mark.asyncio()
@pytest.mark.usefixtures('basic_stream_processor', 'sample_message')
async def test_event_update(mocker, basic_stream_processor, sample_message):
    expected_message = {key: value[:] for key, value in sample_message.items()}
    expected_message['value'].append('python-kafka-streams')
    with asynctest.mock.patch.object(topics[1], 'send'):
        async with basic_stream_processor.agents['pystreams.streams.agents.stream_in'].test_context() as agent:
            event = await agent.put(key='sample', value=sample_message)
            assert agent.results[event.message.offset].value == expected_message
