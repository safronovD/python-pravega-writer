package pravega.connector;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;

public class WriterHttpServer {
    public final PravegaWriter writer;
    public final InetSocketAddress socket;
    public final String endpoint;

    public WriterHttpServer(PravegaWriter writer, InetSocketAddress socket, String endpoint) {
        this.writer = writer;
        this.socket = socket;
        this.endpoint = endpoint;
    }

    public void start() throws IOException {
        HttpServer server = HttpServer.create(socket, 0);
        server.createContext(endpoint, new WriterHttpServer.NewEventHandler(writer));
        server.setExecutor(null);
        server.start();
        System.out.println("PravegaWriter HTTP Server started");
    }

    static class NewEventHandler implements HttpHandler {

        public final PravegaWriter writer;

        public NewEventHandler(PravegaWriter writer) {
            this.writer = writer;
        }

        @Override
        public void handle(HttpExchange httpExchange) throws IOException {
            System.out.println("Write new event from server");

            if (httpExchange.getRequestMethod().equals("POST")) {
                StringBuilder sb = new StringBuilder();
                InputStream ios = httpExchange.getRequestBody();

                writer.newEvent(new String(ios.readAllBytes()));

                httpExchange.sendResponseHeaders(201, -1);
            } else {
                httpExchange.sendResponseHeaders(404, -1);
            }
        }
    }

    public static void main(String[] args) {

        final String scopeName = System.getenv("SCOPE_NAME") == null ? Constants.DEFAULT_SCOPE_NAME : System.getenv("SCOPE_NAME");
        final String streamName = System.getenv("STREAM_NAME") == null ? Constants.DEFAULT_STREAM_NAME : System.getenv("STREAM_NAME");
        final String uriString = System.getenv("CONTROLLER_URI") == null ? Constants.DEFAULT_CONTROLLER_URI : System.getenv("CONTROLLER_URI");
        final URI controllerURI = URI.create(uriString);

        final String routingKey = System.getenv("ROUTING_KEY") == null ? Constants.DEFAULT_ROUTING_KEY : System.getenv("ROUTING_KEY");
        final int serverPort = Integer.parseInt(System.getenv("WRITER_PORT") == null ? Constants.DEFAULT_WRITER_PORT : System.getenv("WRITER_PORT"));
        final String serverEndpoint = System.getenv("WRITER_ENDPOINT") == null ? Constants.DEFAULT_WRITER_ENDPOINT : System.getenv("WRITER_ENDPOINT");

        try {
            //TODO: Make autoclosable
            //close when SIGKILL
            PravegaWriter pw = new PravegaWriter(scopeName, streamName, routingKey, controllerURI);
            WriterHttpServer server = new WriterHttpServer(
                    pw,
                    new InetSocketAddress("0.0.0.0", serverPort),
                    serverEndpoint
            );

            server.start();
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
