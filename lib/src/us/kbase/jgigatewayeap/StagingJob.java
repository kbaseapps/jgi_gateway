
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
 * <p>Original spec-file type: StagingJob</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "jamo_id",
    "filename",
    "username",
    "job_id",
    "status_code",
    "status_raw",
    "created",
    "updated"
})
public class StagingJob {

    @JsonProperty("jamo_id")
    private String jamoId;
    @JsonProperty("filename")
    private String filename;
    @JsonProperty("username")
    private String username;
    @JsonProperty("job_id")
    private String jobId;
    @JsonProperty("status_code")
    private String statusCode;
    @JsonProperty("status_raw")
    private String statusRaw;
    @JsonProperty("created")
    private Long created;
    @JsonProperty("updated")
    private Long updated;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("jamo_id")
    public String getJamoId() {
        return jamoId;
    }

    @JsonProperty("jamo_id")
    public void setJamoId(String jamoId) {
        this.jamoId = jamoId;
    }

    public StagingJob withJamoId(String jamoId) {
        this.jamoId = jamoId;
        return this;
    }

    @JsonProperty("filename")
    public String getFilename() {
        return filename;
    }

    @JsonProperty("filename")
    public void setFilename(String filename) {
        this.filename = filename;
    }

    public StagingJob withFilename(String filename) {
        this.filename = filename;
        return this;
    }

    @JsonProperty("username")
    public String getUsername() {
        return username;
    }

    @JsonProperty("username")
    public void setUsername(String username) {
        this.username = username;
    }

    public StagingJob withUsername(String username) {
        this.username = username;
        return this;
    }

    @JsonProperty("job_id")
    public String getJobId() {
        return jobId;
    }

    @JsonProperty("job_id")
    public void setJobId(String jobId) {
        this.jobId = jobId;
    }

    public StagingJob withJobId(String jobId) {
        this.jobId = jobId;
        return this;
    }

    @JsonProperty("status_code")
    public String getStatusCode() {
        return statusCode;
    }

    @JsonProperty("status_code")
    public void setStatusCode(String statusCode) {
        this.statusCode = statusCode;
    }

    public StagingJob withStatusCode(String statusCode) {
        this.statusCode = statusCode;
        return this;
    }

    @JsonProperty("status_raw")
    public String getStatusRaw() {
        return statusRaw;
    }

    @JsonProperty("status_raw")
    public void setStatusRaw(String statusRaw) {
        this.statusRaw = statusRaw;
    }

    public StagingJob withStatusRaw(String statusRaw) {
        this.statusRaw = statusRaw;
        return this;
    }

    @JsonProperty("created")
    public Long getCreated() {
        return created;
    }

    @JsonProperty("created")
    public void setCreated(Long created) {
        this.created = created;
    }

    public StagingJob withCreated(Long created) {
        this.created = created;
        return this;
    }

    @JsonProperty("updated")
    public Long getUpdated() {
        return updated;
    }

    @JsonProperty("updated")
    public void setUpdated(Long updated) {
        this.updated = updated;
    }

    public StagingJob withUpdated(Long updated) {
        this.updated = updated;
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
        return ((((((((((((((((((("StagingJob"+" [jamoId=")+ jamoId)+", filename=")+ filename)+", username=")+ username)+", jobId=")+ jobId)+", statusCode=")+ statusCode)+", statusRaw=")+ statusRaw)+", created=")+ created)+", updated=")+ updated)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
