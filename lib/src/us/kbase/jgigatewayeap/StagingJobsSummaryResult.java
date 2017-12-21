
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
 * <p>Original spec-file type: StagingJobsSummaryResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "state"
})
public class StagingJobsSummaryResult {

    @JsonProperty("state")
    private Map<String, StagingJobsSummary> state;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("state")
    public Map<String, StagingJobsSummary> getState() {
        return state;
    }

    @JsonProperty("state")
    public void setState(Map<String, StagingJobsSummary> state) {
        this.state = state;
    }

    public StagingJobsSummaryResult withState(Map<String, StagingJobsSummary> state) {
        this.state = state;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((("StagingJobsSummaryResult"+" [state=")+ state)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
