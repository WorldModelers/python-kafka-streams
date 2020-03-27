import faust
from faust.streams import Stream


app = faust.App('pystreams',
                broker='kafka://kafka-broker-1:19092',
                autodiscover=True,
                origin='pystreams')


import pystreams.streams.agents


def main() -> None:
    app.main()
