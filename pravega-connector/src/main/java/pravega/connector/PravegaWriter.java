package pravega.connector;

import java.net.URI;
import java.util.concurrent.CompletableFuture;

import io.pravega.client.ClientConfig;

import io.pravega.client.EventStreamClientFactory;
import io.pravega.client.admin.StreamManager;
import io.pravega.client.stream.EventStreamWriter;
import io.pravega.client.stream.EventWriterConfig;
import io.pravega.client.stream.ScalingPolicy;
import io.pravega.client.stream.StreamConfiguration;
import io.pravega.client.stream.impl.JavaSerializer;

public class PravegaWriter implements AutoCloseable {
    public final String scopeName;
    public final String streamName;
    public final URI controllerURI;

    public final String routingKey;
    public final EventStreamWriter<String> writer;

    public PravegaWriter(String scopeName, String streamName, String routingKey, URI controllerURI) {

        this.scopeName = scopeName;
        this.streamName = streamName;
        this.controllerURI = controllerURI;

        this.routingKey = routingKey;

        //Create new scope and stream
        //Remove after operator will be added
        StreamManager streamManager = StreamManager.create(controllerURI);
        final boolean scopeIsNew = streamManager.createScope(scopeName);

        StreamConfiguration streamConfig = StreamConfiguration.builder()
                .scalingPolicy(ScalingPolicy.fixed(1))
                .build();
        final boolean streamIsNew = streamManager.createStream(scopeName, streamName, streamConfig);

        EventStreamWriter<String> tempWriter = null;
        try {
            EventStreamClientFactory clientFactory = EventStreamClientFactory.withScope(
                    scopeName,
                    ClientConfig.builder().controllerURI(controllerURI).build()
            );

             tempWriter = clientFactory.createEventWriter(
                     streamName,
                     new JavaSerializer<String>(),
                     EventWriterConfig.builder().build()
             );
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
        this.writer = tempWriter;
    }

    @Override
    public void close() {
        writer.close();
    }

    public void newEvent(String message) {
        System.out.format("Writing message: '%s' with routing-key: '%s' to stream '%s / %s'%n",
                message, routingKey, scopeName, streamName);
        final CompletableFuture writeFuture = writer.writeEvent(routingKey, message);
    }
}

