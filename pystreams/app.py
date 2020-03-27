import faust


# create your application. here we give it a name and broker. the other two
# arguments allow faust to find everything else neeeded
app = faust.App('pystreams',
                broker='kafka://kafka-broker-1:19092',
                autodiscover=True,
                origin='pystreams')


# this import seems weird, but we simply need to ensure that the agents (and
# topics) are loaded explicitly after our app is created. faust's autodiscovery
# takes care of the rest. in a more complex project this could be done more
# cleanly
import pystreams.streams.agents  # noqa: E402, F401


# used for a main entrypoint
def main() -> None:
    app.main()
