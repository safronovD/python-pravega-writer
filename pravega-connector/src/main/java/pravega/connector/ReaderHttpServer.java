package pravega.connector;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.*;
import java.net.InetSocketAddress;
import java.net.URI;

public class ReaderHttpServer {

    public final PravegaReader reader;
    public final InetSocketAddress socket;
    public final String endpoint;

    public ReaderHttpServer(PravegaReader reader, InetSocketAddress socket, String endpoint) {
        this.reader = reader;
        this.socket = socket;
        this.endpoint = endpoint;
    }

    public void start() throws IOException {
        HttpServer server = HttpServer.create(socket, 0);
        server.createContext(endpoint, new NextEventHandler(reader));
        server.setExecutor(null);
        server.start();
        System.out.println("PravegaReader HTTP Server started");
    }

    static class NextEventHandler implements HttpHandler {

        public final PravegaReader reader;

        public NextEventHandler(PravegaReader reader) {
            this.reader = reader;
        }

        @Override
        public void handle(HttpExchange httpExchange) throws IOException {
            System.out.println("Try new event from server");

            String event = reader.nextEvent();
            String response;

            if (event != null) {
                response = event;
                httpExchange.sendResponseHeaders(200, response.length());
            } else {
                response = "";
                httpExchange.sendResponseHeaders(204, -1);
            }

            OutputStream os = httpExchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }

    public static void main(String[] args) {

        final String scopeName = System.getenv("SCOPE_NAME") == null ? Constants.DEFAULT_SCOPE_NAME : System.getenv("SCOPE_NAME");
        final String streamName = System.getenv("STREAM_NAME") == null ? Constants.DEFAULT_STREAM_NAME : System.getenv("STREAM_NAME");
        final String uriString = System.getenv("CONTROLLER_URI") == null ? Constants.DEFAULT_CONTROLLER_URI : System.getenv("CONTROLLER_URI");
        final URI controllerURI = URI.create(uriString);

        final String readerGroup = System.getenv("READER_GROUP") == null ? Constants.DEFAULT_READER_GROUP : System.getenv("READER_GROUP");
        final int serverPort = Integer.parseInt(System.getenv("READER_PORT") == null ? Constants.DEFAULT_READER_PORT : System.getenv("READER_PORT"));
        final String serverEndpoint = System.getenv("READER_ENDPOINT") == null ? Constants.DEFAULT_READER_ENDPOINT : System.getenv("READER_ENDPOINT");

        try {
            //TODO: Make autoclosable
            //close when SIGKILL
            PravegaReader pr = new PravegaReader(scopeName, streamName, readerGroup, controllerURI);
            ReaderHttpServer server = new ReaderHttpServer(
                    pr,
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
