
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
 * <p>Original spec-file type: StagingStatusInput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "job_monitoring_id"
})
public class StagingStatusInput {

    @JsonProperty("job_monitoring_id")
    private String jobMonitoringId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("job_monitoring_id")
    public String getJobMonitoringId() {
        return jobMonitoringId;
    }

    @JsonProperty("job_monitoring_id")
    public void setJobMonitoringId(String jobMonitoringId) {
        this.jobMonitoringId = jobMonitoringId;
    }

    public StagingStatusInput withJobMonitoringId(String jobMonitoringId) {
        this.jobMonitoringId = jobMonitoringId;
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
        return ((((("StagingStatusInput"+" [jobMonitoringId=")+ jobMonitoringId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
