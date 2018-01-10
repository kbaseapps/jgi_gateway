
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
 * <p>Original spec-file type: RemoveStagingJobInput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "username",
    "job_monitoring_id"
})
public class RemoveStagingJobInput {

    @JsonProperty("username")
    private String username;
    @JsonProperty("job_monitoring_id")
    private String jobMonitoringId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("username")
    public String getUsername() {
        return username;
    }

    @JsonProperty("username")
    public void setUsername(String username) {
        this.username = username;
    }

    public RemoveStagingJobInput withUsername(String username) {
        this.username = username;
        return this;
    }

    @JsonProperty("job_monitoring_id")
    public String getJobMonitoringId() {
        return jobMonitoringId;
    }

    @JsonProperty("job_monitoring_id")
    public void setJobMonitoringId(String jobMonitoringId) {
        this.jobMonitoringId = jobMonitoringId;
    }

    public RemoveStagingJobInput withJobMonitoringId(String jobMonitoringId) {
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
        return ((((((("RemoveStagingJobInput"+" [username=")+ username)+", jobMonitoringId=")+ jobMonitoringId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
