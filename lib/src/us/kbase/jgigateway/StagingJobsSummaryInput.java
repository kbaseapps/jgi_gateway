
package us.kbase.jgigateway;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: StagingJobsSummaryInput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "username",
    "job_monitoring_ids"
})
public class StagingJobsSummaryInput {

    @JsonProperty("username")
    private java.lang.String username;
    @JsonProperty("job_monitoring_ids")
    private List<String> jobMonitoringIds;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("username")
    public java.lang.String getUsername() {
        return username;
    }

    @JsonProperty("username")
    public void setUsername(java.lang.String username) {
        this.username = username;
    }

    public StagingJobsSummaryInput withUsername(java.lang.String username) {
        this.username = username;
        return this;
    }

    @JsonProperty("job_monitoring_ids")
    public List<String> getJobMonitoringIds() {
        return jobMonitoringIds;
    }

    @JsonProperty("job_monitoring_ids")
    public void setJobMonitoringIds(List<String> jobMonitoringIds) {
        this.jobMonitoringIds = jobMonitoringIds;
    }

    public StagingJobsSummaryInput withJobMonitoringIds(List<String> jobMonitoringIds) {
        this.jobMonitoringIds = jobMonitoringIds;
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
        return ((((((("StagingJobsSummaryInput"+" [username=")+ username)+", jobMonitoringIds=")+ jobMonitoringIds)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
