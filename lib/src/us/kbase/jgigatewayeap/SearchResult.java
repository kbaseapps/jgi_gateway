
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

    /**
     * <p>Original spec-file type: SearchQueryResult</p>
     * <pre>
     * SearchQueryResult
     * The top level search object returned from the query.
     * Note that this structure closely parallels that returned by the jgi search service.
     * The only functional difference is that some field names which were prefixed by 
     * underscore are known by their unprefixed selfs.
     * hits  - a list of the actual search result documents and statsitics returned;;
     *         note that this represents the window of search results defined by
     *         the limit input property.
     * total - the total number of items matched by the search; not the same as the 
     *        items actually returned;
     * </pre>
     * 
     */
    @JsonProperty("search_result")
    private SearchQueryResult searchResult;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: SearchQueryResult</p>
     * <pre>
     * SearchQueryResult
     * The top level search object returned from the query.
     * Note that this structure closely parallels that returned by the jgi search service.
     * The only functional difference is that some field names which were prefixed by 
     * underscore are known by their unprefixed selfs.
     * hits  - a list of the actual search result documents and statsitics returned;;
     *         note that this represents the window of search results defined by
     *         the limit input property.
     * total - the total number of items matched by the search; not the same as the 
     *        items actually returned;
     * </pre>
     * 
     */
    @JsonProperty("search_result")
    public SearchQueryResult getSearchResult() {
        return searchResult;
    }

    /**
     * <p>Original spec-file type: SearchQueryResult</p>
     * <pre>
     * SearchQueryResult
     * The top level search object returned from the query.
     * Note that this structure closely parallels that returned by the jgi search service.
     * The only functional difference is that some field names which were prefixed by 
     * underscore are known by their unprefixed selfs.
     * hits  - a list of the actual search result documents and statsitics returned;;
     *         note that this represents the window of search results defined by
     *         the limit input property.
     * total - the total number of items matched by the search; not the same as the 
     *        items actually returned;
     * </pre>
     * 
     */
    @JsonProperty("search_result")
    public void setSearchResult(SearchQueryResult searchResult) {
        this.searchResult = searchResult;
    }

    public SearchResult withSearchResult(SearchQueryResult searchResult) {
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
