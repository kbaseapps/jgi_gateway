
package us.kbase.jgigatewayeap;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: SearchResultItem</p>
 * <pre>
 * SearchResult
 * Represents a single search result item
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "source",
    "index",
    "score",
    "id"
})
public class SearchResultItem {

    @JsonProperty("source")
    private UObject source;
    @JsonProperty("index")
    private String index;
    @JsonProperty("score")
    private String score;
    @JsonProperty("id")
    private String id;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("source")
    public UObject getSource() {
        return source;
    }

    @JsonProperty("source")
    public void setSource(UObject source) {
        this.source = source;
    }

    public SearchResultItem withSource(UObject source) {
        this.source = source;
        return this;
    }

    @JsonProperty("index")
    public String getIndex() {
        return index;
    }

    @JsonProperty("index")
    public void setIndex(String index) {
        this.index = index;
    }

    public SearchResultItem withIndex(String index) {
        this.index = index;
        return this;
    }

    @JsonProperty("score")
    public String getScore() {
        return score;
    }

    @JsonProperty("score")
    public void setScore(String score) {
        this.score = score;
    }

    public SearchResultItem withScore(String score) {
        this.score = score;
        return this;
    }

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public SearchResultItem withId(String id) {
        this.id = id;
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
        return ((((((((((("SearchResultItem"+" [source=")+ source)+", index=")+ index)+", score=")+ score)+", id=")+ id)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
