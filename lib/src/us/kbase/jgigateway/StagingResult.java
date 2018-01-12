
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
 * <p>Original spec-file type: StagingResult</p>
 * <pre>
 * StagingResult returns a map entry for each id submitted in the stage request.
 * The map key is the _id property returned in a SearchResult item (not described here but probably 
 * should be), the value is a string describing the result of the staging request.
 * At time of writing, the value is always "staging" since the request to the jgi gateway jgi service
 * and the call to stage in the jgi gateway kbase service are in different processes.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "job_id",
    "job_monitoring_id"
})
public class StagingResult {

    @JsonProperty("job_id")
    private String jobId;
    @JsonProperty("job_monitoring_id")
    private String jobMonitoringId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("job_id")
    public String getJobId() {
        return jobId;
    }

    @JsonProperty("job_id")
    public void setJobId(String jobId) {
        this.jobId = jobId;
    }

    public StagingResult withJobId(String jobId) {
        this.jobId = jobId;
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

    public StagingResult withJobMonitoringId(String jobMonitoringId) {
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
        return ((((((("StagingResult"+" [jobId=")+ jobId)+", jobMonitoringId=")+ jobMonitoringId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
