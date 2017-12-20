
package us.kbase.jgigatewayeap;

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
 * <p>Original spec-file type: StagingJobsResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "staging_jobs",
    "total_matched",
    "total_jobs"
})
public class StagingJobsResult {

    @JsonProperty("staging_jobs")
    private List<StagingJob> stagingJobs;
    @JsonProperty("total_matched")
    private Long totalMatched;
    @JsonProperty("total_jobs")
    private Long totalJobs;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("staging_jobs")
    public List<StagingJob> getStagingJobs() {
        return stagingJobs;
    }

    @JsonProperty("staging_jobs")
    public void setStagingJobs(List<StagingJob> stagingJobs) {
        this.stagingJobs = stagingJobs;
    }

    public StagingJobsResult withStagingJobs(List<StagingJob> stagingJobs) {
        this.stagingJobs = stagingJobs;
        return this;
    }

    @JsonProperty("total_matched")
    public Long getTotalMatched() {
        return totalMatched;
    }

    @JsonProperty("total_matched")
    public void setTotalMatched(Long totalMatched) {
        this.totalMatched = totalMatched;
    }

    public StagingJobsResult withTotalMatched(Long totalMatched) {
        this.totalMatched = totalMatched;
        return this;
    }

    @JsonProperty("total_jobs")
    public Long getTotalJobs() {
        return totalJobs;
    }

    @JsonProperty("total_jobs")
    public void setTotalJobs(Long totalJobs) {
        this.totalJobs = totalJobs;
    }

    public StagingJobsResult withTotalJobs(Long totalJobs) {
        this.totalJobs = totalJobs;
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
        return ((((((((("StagingJobsResult"+" [stagingJobs=")+ stagingJobs)+", totalMatched=")+ totalMatched)+", totalJobs=")+ totalJobs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
