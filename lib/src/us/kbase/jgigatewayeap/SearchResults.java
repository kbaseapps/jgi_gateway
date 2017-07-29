
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
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: SearchResults</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "search_result",
    "search_elapsed_time"
})
public class SearchResults {

    @JsonProperty("search_result")
    private List<UObject> searchResult;
    @JsonProperty("search_elapsed_time")
    private Long searchElapsedTime;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("search_result")
    public List<UObject> getSearchResult() {
        return searchResult;
    }

    @JsonProperty("search_result")
    public void setSearchResult(List<UObject> searchResult) {
        this.searchResult = searchResult;
    }

    public SearchResults withSearchResult(List<UObject> searchResult) {
        this.searchResult = searchResult;
        return this;
    }

    @JsonProperty("search_elapsed_time")
    public Long getSearchElapsedTime() {
        return searchElapsedTime;
    }

    @JsonProperty("search_elapsed_time")
    public void setSearchElapsedTime(Long searchElapsedTime) {
        this.searchElapsedTime = searchElapsedTime;
    }

    public SearchResults withSearchElapsedTime(Long searchElapsedTime) {
        this.searchElapsedTime = searchElapsedTime;
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
        return ((((((("SearchResults"+" [searchResult=")+ searchResult)+", searchElapsedTime=")+ searchElapsedTime)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
