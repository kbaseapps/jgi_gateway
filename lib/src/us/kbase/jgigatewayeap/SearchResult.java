
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
 * <p>Original spec-file type: SearchResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "search_result"
})
public class SearchResult {

    @JsonProperty("search_result")
    private List<UObject> searchResult;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("search_result")
    public List<UObject> getSearchResult() {
        return searchResult;
    }

    @JsonProperty("search_result")
    public void setSearchResult(List<UObject> searchResult) {
        this.searchResult = searchResult;
    }

    public SearchResult withSearchResult(List<UObject> searchResult) {
        this.searchResult = searchResult;
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
        return ((((("SearchResult"+" [searchResult=")+ searchResult)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
