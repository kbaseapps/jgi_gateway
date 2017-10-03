
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
 * <p>Original spec-file type: SearchInput</p>
 * <pre>
 * search_jgi searches the JGI service for matches against the
 * search_string
 * Other parameters
 * @optional limit
 * @optional page
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "search_string",
    "filter",
    "limit",
    "page",
    "include_private"
})
public class SearchInput {

    @JsonProperty("search_string")
    private java.lang.String searchString;
    @JsonProperty("filter")
    private Map<String, UObject> filter;
    @JsonProperty("limit")
    private Long limit;
    @JsonProperty("page")
    private Long page;
    @JsonProperty("include_private")
    private Long includePrivate;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("search_string")
    public java.lang.String getSearchString() {
        return searchString;
    }

    @JsonProperty("search_string")
    public void setSearchString(java.lang.String searchString) {
        this.searchString = searchString;
    }

    public SearchInput withSearchString(java.lang.String searchString) {
        this.searchString = searchString;
        return this;
    }

    @JsonProperty("filter")
    public Map<String, UObject> getFilter() {
        return filter;
    }

    @JsonProperty("filter")
    public void setFilter(Map<String, UObject> filter) {
        this.filter = filter;
    }

    public SearchInput withFilter(Map<String, UObject> filter) {
        this.filter = filter;
        return this;
    }

    @JsonProperty("limit")
    public Long getLimit() {
        return limit;
    }

    @JsonProperty("limit")
    public void setLimit(Long limit) {
        this.limit = limit;
    }

    public SearchInput withLimit(Long limit) {
        this.limit = limit;
        return this;
    }

    @JsonProperty("page")
    public Long getPage() {
        return page;
    }

    @JsonProperty("page")
    public void setPage(Long page) {
        this.page = page;
    }

    public SearchInput withPage(Long page) {
        this.page = page;
        return this;
    }

    @JsonProperty("include_private")
    public Long getIncludePrivate() {
        return includePrivate;
    }

    @JsonProperty("include_private")
    public void setIncludePrivate(Long includePrivate) {
        this.includePrivate = includePrivate;
    }

    public SearchInput withIncludePrivate(Long includePrivate) {
        this.includePrivate = includePrivate;
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
        return ((((((((((((("SearchInput"+" [searchString=")+ searchString)+", filter=")+ filter)+", limit=")+ limit)+", page=")+ page)+", includePrivate=")+ includePrivate)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
