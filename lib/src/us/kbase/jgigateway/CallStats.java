
package us.kbase.jgigateway;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: CallStats</p>
 * <pre>
 * Call performance measurement
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "request_elapsed_time"
})
public class CallStats {

    @JsonProperty("request_elapsed_time")
    private Long requestElapsedTime;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("request_elapsed_time")
    public Long getRequestElapsedTime() {
        return requestElapsedTime;
    }

    @JsonProperty("request_elapsed_time")
    public void setRequestElapsedTime(Long requestElapsedTime) {
        this.requestElapsedTime = requestElapsedTime;
    }

    public CallStats withRequestElapsedTime(Long requestElapsedTime) {
        this.requestElapsedTime = requestElapsedTime;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((("CallStats"+" [requestElapsedTime=")+ requestElapsedTime)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
