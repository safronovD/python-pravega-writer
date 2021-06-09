package pravega.connector;

import java.net.InetAddress;
import java.net.URI;
import java.net.UnknownHostException;
import java.util.UUID;

import io.pravega.client.ClientConfig;
import io.pravega.client.stream.Stream;

import io.pravega.client.EventStreamClientFactory;
import io.pravega.client.admin.ReaderGroupManager;
import io.pravega.client.stream.EventRead;
import io.pravega.client.stream.EventStreamReader;
import io.pravega.client.stream.ReaderConfig;
import io.pravega.client.stream.ReaderGroupConfig;
import io.pravega.client.stream.ReinitializationRequiredException;
import io.pravega.client.stream.impl.JavaSerializer;

public class PravegaReader implements AutoCloseable {
    private static final int READER_TIMEOUT_MS = 2000;

    public final String scopeName;
    public final String streamName;
    public final URI controllerURI;
    public final String readerGroup;

    public final String readerID;
    public final EventStreamReader<String> reader;

    public PravegaReader(String scopeName, String streamName, String readerGroup, URI controllerURI) {

        this.scopeName = scopeName;
        this.streamName = streamName;
        this.controllerURI = controllerURI;
        this.readerGroup = readerGroup;

        //Need unique readerID for each reader in group
        String tempReaderID;
        try {
            //Temporary
            //Until close method would call correctly
            tempReaderID = UUID.randomUUID().toString().replace("-", "");
            //InetAddress ip = InetAddress.getLocalHost();
            //tempReaderID = ip.getHostName();
        } catch (Exception e) { //UnknownHostException
            e.printStackTrace();
            tempReaderID = UUID.randomUUID().toString().replace("-", "");
        }
        this.readerID = tempReaderID;

        //Create ReaderGroup if not exists
        final ReaderGroupConfig readerGroupConfig = ReaderGroupConfig.builder()
                .stream(Stream.of(scopeName, streamName))
                .build();
        try (ReaderGroupManager readerGroupManager = ReaderGroupManager.withScope(scopeName, controllerURI)) {
            readerGroupManager.createReaderGroup(readerGroup, readerGroupConfig);
        }

        EventStreamReader<String> tempReader = null;
        try {
            EventStreamClientFactory clientFactory = EventStreamClientFactory.withScope(
                    scopeName,
                    ClientConfig.builder().controllerURI(controllerURI).build()
            );

            tempReader = clientFactory.createReader(
                    readerID,
                    readerGroup,
                    new JavaSerializer<String>(),
                    ReaderConfig.builder().build()
            );
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
        this.reader = tempReader;
    }

    @Override
    public void close() {
        reader.close();
    }

    public String nextEvent() {
        System.out.println("Try new event from reader");

        EventRead<String> event = null;
        try {
            event = reader.readNextEvent(READER_TIMEOUT_MS);
            if (event.getEvent() != null) {
                System.out.format("Read event '%s'%n", event.getEvent());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return event.getEvent();
    }
}