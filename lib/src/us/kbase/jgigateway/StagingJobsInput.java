
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
 * <p>Original spec-file type: StagingJobsInput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "filter",
    "range",
    "sort"
})
public class StagingJobsInput {

    /**
     * <p>Original spec-file type: StagingJobsFilter</p>
     * 
     * 
     */
    @JsonProperty("filter")
    private StagingJobsFilter filter;
    /**
     * <p>Original spec-file type: StagingJobsRange</p>
     * 
     * 
     */
    @JsonProperty("range")
    private StagingJobsRange range;
    @JsonProperty("sort")
    private List<SortSpec> sort;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: StagingJobsFilter</p>
     * 
     * 
     */
    @JsonProperty("filter")
    public StagingJobsFilter getFilter() {
        return filter;
    }

    /**
     * <p>Original spec-file type: StagingJobsFilter</p>
     * 
     * 
     */
    @JsonProperty("filter")
    public void setFilter(StagingJobsFilter filter) {
        this.filter = filter;
    }

    public StagingJobsInput withFilter(StagingJobsFilter filter) {
        this.filter = filter;
        return this;
    }

    /**
     * <p>Original spec-file type: StagingJobsRange</p>
     * 
     * 
     */
    @JsonProperty("range")
    public StagingJobsRange getRange() {
        return range;
    }

    /**
     * <p>Original spec-file type: StagingJobsRange</p>
     * 
     * 
     */
    @JsonProperty("range")
    public void setRange(StagingJobsRange range) {
        this.range = range;
    }

    public StagingJobsInput withRange(StagingJobsRange range) {
        this.range = range;
        return this;
    }

    @JsonProperty("sort")
    public List<SortSpec> getSort() {
        return sort;
    }

    @JsonProperty("sort")
    public void setSort(List<SortSpec> sort) {
        this.sort = sort;
    }

    public StagingJobsInput withSort(List<SortSpec> sort) {
        this.sort = sort;
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
        return ((((((((("StagingJobsInput"+" [filter=")+ filter)+", range=")+ range)+", sort=")+ sort)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
