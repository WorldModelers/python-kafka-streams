import ssl
import faust
from pystreams import config
from pystreams.streams.agents import create_streams


app = None


def create_app():
    broker = None
    if config.get('broker'):
        broker = f'kafka://{config["broker"]}',

    broker_credentials = None
    if 'auth' in config:
        broker_credentials = faust.SASLCredentials(
            username=config['auth']['username'],
            password=config['auth']['password'],
            ssl_context=ssl.create_default_context()
        )

    # create your application
    global app
    app = faust.App(
        config['app']['id'],
        autodiscover=True,
        origin='pystreams',
        broker=broker,
        broker_credentials=broker_credentials,
        consumer_auto_offset_reset=config['app'].get('auto_offset_reset', None),
        stream_wait_empty=config['app'].get('enable_auto_commit', None),
        topic_disable_leader=True
    )
    topics = create_streams(app)
    return app, topics


# used for a main entrypoint
def main() -> None:
    app.main()
