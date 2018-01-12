
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
 * <p>Original spec-file type: StageInput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "file"
})
public class StageInput {

    /**
     * <p>Original spec-file type: StageRequest</p>
     * <pre>
     * STAGE
     * </pre>
     * 
     */
    @JsonProperty("file")
    private StageRequest file;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: StageRequest</p>
     * <pre>
     * STAGE
     * </pre>
     * 
     */
    @JsonProperty("file")
    public StageRequest getFile() {
        return file;
    }

    /**
     * <p>Original spec-file type: StageRequest</p>
     * <pre>
     * STAGE
     * </pre>
     * 
     */
    @JsonProperty("file")
    public void setFile(StageRequest file) {
        this.file = file;
    }

    public StageInput withFile(StageRequest file) {
        this.file = file;
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
        return ((((("StageInput"+" [file=")+ file)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
