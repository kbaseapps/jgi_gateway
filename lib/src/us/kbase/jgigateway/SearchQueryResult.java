
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
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "hits",
    "total"
})
public class SearchQueryResult {

    @JsonProperty("hits")
    private List<SearchResultItem> hits;
    @JsonProperty("total")
    private Long total;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("hits")
    public List<SearchResultItem> getHits() {
        return hits;
    }

    @JsonProperty("hits")
    public void setHits(List<SearchResultItem> hits) {
        this.hits = hits;
    }

    public SearchQueryResult withHits(List<SearchResultItem> hits) {
        this.hits = hits;
        return this;
    }

    @JsonProperty("total")
    public Long getTotal() {
        return total;
    }

    @JsonProperty("total")
    public void setTotal(Long total) {
        this.total = total;
    }

    public SearchQueryResult withTotal(Long total) {
        this.total = total;
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
        return ((((((("SearchQueryResult"+" [hits=")+ hits)+", total=")+ total)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
