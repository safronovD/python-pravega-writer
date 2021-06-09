package pravega.connector;

public class Constants {
    protected static final String DEFAULT_SCOPE_NAME = "ppwDefault";
    protected static final String DEFAULT_STREAM_NAME = "ppwDefault";
    protected static final String DEFAULT_CONTROLLER_URI = "tcp://127.0.0.1:9090";

    protected static final String DEFAULT_READER_GROUP = "ppwDefault";
    protected static final String DEFAULT_READER_PORT = "8661";
    protected static final String DEFAULT_READER_ENDPOINT = "/nextEvent";

    protected static final String DEFAULT_ROUTING_KEY = "SameRoutingKey";
    protected static final String DEFAULT_WRITER_PORT = "8662";
    protected static final String DEFAULT_WRITER_ENDPOINT = "/newEvent";
}
