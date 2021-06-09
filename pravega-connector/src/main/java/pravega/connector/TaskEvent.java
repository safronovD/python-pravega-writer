package pravega.connector;

import com.google.gson.JsonObject;
import io.pravega.keycloak.com.fasterxml.jackson.core.JsonProcessingException;
import io.pravega.keycloak.com.fasterxml.jackson.databind.ObjectMapper;

import java.io.Serializable;

public class TaskEvent implements Serializable {

    private String id;
    private String text;

    public TaskEvent(String id, String text) {
        this.id = id;
        this.text = text;
    }

    @Override
    public String toString() {
        String jsonString = "";
        ObjectMapper mapper = new ObjectMapper();
        try {
            jsonString = mapper.writeValueAsString(this);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        return jsonString;
    }
}
