
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
    "states",
    "ids_states"
})
public class StagingJobsSummaryResult {

    @JsonProperty("states")
    private Map<String, us.kbase.jgigatewayeap.StagingJobsSummary> states;
    @JsonProperty("ids_states")
    private Map<String, Map<String, us.kbase.jgigatewayeap.StagingJobsSummary>> idsStates;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("states")
    public Map<String, us.kbase.jgigatewayeap.StagingJobsSummary> getStates() {
        return states;
    }

    @JsonProperty("states")
    public void setStates(Map<String, us.kbase.jgigatewayeap.StagingJobsSummary> states) {
        this.states = states;
    }

    public StagingJobsSummaryResult withStates(Map<String, us.kbase.jgigatewayeap.StagingJobsSummary> states) {
        this.states = states;
        return this;
    }

    @JsonProperty("ids_states")
    public Map<String, Map<String, us.kbase.jgigatewayeap.StagingJobsSummary>> getIdsStates() {
        return idsStates;
    }

    @JsonProperty("ids_states")
    public void setIdsStates(Map<String, Map<String, us.kbase.jgigatewayeap.StagingJobsSummary>> idsStates) {
        this.idsStates = idsStates;
    }

    public StagingJobsSummaryResult withIdsStates(Map<String, Map<String, us.kbase.jgigatewayeap.StagingJobsSummary>> idsStates) {
        this.idsStates = idsStates;
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
        return ((((((("StagingJobsSummaryResult"+" [states=")+ states)+", idsStates=")+ idsStates)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
