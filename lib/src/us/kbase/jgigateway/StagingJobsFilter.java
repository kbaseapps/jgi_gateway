
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
 * <p>Original spec-file type: StagingJobsFilter</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "created_from",
    "created_to",
    "updated_from",
    "updated_to",
    "status",
    "id",
    "job_ids",
    "job_monitoring_ids",
    "filename"
})
public class StagingJobsFilter {

    @JsonProperty("created_from")
    private Long createdFrom;
    @JsonProperty("created_to")
    private Long createdTo;
    @JsonProperty("updated_from")
    private Long updatedFrom;
    @JsonProperty("updated_to")
    private Long updatedTo;
    @JsonProperty("status")
    private java.lang.String status;
    @JsonProperty("id")
    private java.lang.String id;
    @JsonProperty("job_ids")
    private List<String> jobIds;
    @JsonProperty("job_monitoring_ids")
    private List<String> jobMonitoringIds;
    @JsonProperty("filename")
    private java.lang.String filename;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("created_from")
    public Long getCreatedFrom() {
        return createdFrom;
    }

    @JsonProperty("created_from")
    public void setCreatedFrom(Long createdFrom) {
        this.createdFrom = createdFrom;
    }

    public StagingJobsFilter withCreatedFrom(Long createdFrom) {
        this.createdFrom = createdFrom;
        return this;
    }

    @JsonProperty("created_to")
    public Long getCreatedTo() {
        return createdTo;
    }

    @JsonProperty("created_to")
    public void setCreatedTo(Long createdTo) {
        this.createdTo = createdTo;
    }

    public StagingJobsFilter withCreatedTo(Long createdTo) {
        this.createdTo = createdTo;
        return this;
    }

    @JsonProperty("updated_from")
    public Long getUpdatedFrom() {
        return updatedFrom;
    }

    @JsonProperty("updated_from")
    public void setUpdatedFrom(Long updatedFrom) {
        this.updatedFrom = updatedFrom;
    }

    public StagingJobsFilter withUpdatedFrom(Long updatedFrom) {
        this.updatedFrom = updatedFrom;
        return this;
    }

    @JsonProperty("updated_to")
    public Long getUpdatedTo() {
        return updatedTo;
    }

    @JsonProperty("updated_to")
    public void setUpdatedTo(Long updatedTo) {
        this.updatedTo = updatedTo;
    }

    public StagingJobsFilter withUpdatedTo(Long updatedTo) {
        this.updatedTo = updatedTo;
        return this;
    }

    @JsonProperty("status")
    public java.lang.String getStatus() {
        return status;
    }

    @JsonProperty("status")
    public void setStatus(java.lang.String status) {
        this.status = status;
    }

    public StagingJobsFilter withStatus(java.lang.String status) {
        this.status = status;
        return this;
    }

    @JsonProperty("id")
    public java.lang.String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(java.lang.String id) {
        this.id = id;
    }

    public StagingJobsFilter withId(java.lang.String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("job_ids")
    public List<String> getJobIds() {
        return jobIds;
    }

    @JsonProperty("job_ids")
    public void setJobIds(List<String> jobIds) {
        this.jobIds = jobIds;
    }

    public StagingJobsFilter withJobIds(List<String> jobIds) {
        this.jobIds = jobIds;
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

    public StagingJobsFilter withJobMonitoringIds(List<String> jobMonitoringIds) {
        this.jobMonitoringIds = jobMonitoringIds;
        return this;
    }

    @JsonProperty("filename")
    public java.lang.String getFilename() {
        return filename;
    }

    @JsonProperty("filename")
    public void setFilename(java.lang.String filename) {
        this.filename = filename;
    }

    public StagingJobsFilter withFilename(java.lang.String filename) {
        this.filename = filename;
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
        return ((((((((((((((((((((("StagingJobsFilter"+" [createdFrom=")+ createdFrom)+", createdTo=")+ createdTo)+", updatedFrom=")+ updatedFrom)+", updatedTo=")+ updatedTo)+", status=")+ status)+", id=")+ id)+", jobIds=")+ jobIds)+", jobMonitoringIds=")+ jobMonitoringIds)+", filename=")+ filename)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
