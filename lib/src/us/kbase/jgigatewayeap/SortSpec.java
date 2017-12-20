
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
 * <p>Original spec-file type: SortSpec</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "field",
    "descending"
})
public class SortSpec {

    @JsonProperty("field")
    private String field;
    @JsonProperty("descending")
    private Long descending;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("field")
    public String getField() {
        return field;
    }

    @JsonProperty("field")
    public void setField(String field) {
        this.field = field;
    }

    public SortSpec withField(String field) {
        this.field = field;
        return this;
    }

    @JsonProperty("descending")
    public Long getDescending() {
        return descending;
    }

    @JsonProperty("descending")
    public void setDescending(Long descending) {
        this.descending = descending;
    }

    public SortSpec withDescending(Long descending) {
        this.descending = descending;
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
        return ((((((("SortSpec"+" [field=")+ field)+", descending=")+ descending)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
