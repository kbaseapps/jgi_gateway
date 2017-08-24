
package us.kbase.jgigatewayeap;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: StagingStatusResult</p>
 * <pre>
 * should be:
 * typedef structure {
 *     int queued;
 *     int in_progress;
 *     int copy_in_progress;
 *     int restore_failed;
 *     in scp_failed
 * } StagingStatusResult;
 * funcdef stage_status(string job_id) 
 *         returns (StagingStatusResult result, CallStats stats) 
 *         authentication required;
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "message"
})
public class StagingStatusResult {

    @JsonProperty("message")
    private String message;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("message")
    public String getMessage() {
        return message;
    }

    @JsonProperty("message")
    public void setMessage(String message) {
        this.message = message;
    }

    public StagingStatusResult withMessage(String message) {
        this.message = message;
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
        return ((((("StagingStatusResult"+" [message=")+ message)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
