# JGI Gateway API

## search_jgi

The ```search_jgi``` method is the only entrypoint for conducting searches against the JGI JAMO Search Service.

### Input

The input is provided in the form of a single json object as the first parameter.

The only required input is the ```query``` property, which contains the query specification itself. All other input properties are optional and have default values.

Below is an example query object:

```json
{
    "query": {"_all": "coli", "file_type": "fastq", "operator": "AND"},
    "filter": {"project_id": 123},
    "limit": 25,
    "page": 3,
    "include_private": 1
}
```

Now we'll describe each top level property.

#### query

The query property is the only required property. It specifies query expressions to be applied against individual fields. The query expression syntax is described bleow. 

The optional "operator" property indicates a boolean operation to be applied to all of the search expressions. It may be "AND", "OR", or "NOT". It defaults to "OR".

The "_all" search field is special - it corresponds to a special search field built up from all other fields in the indexed document.

##### query string syntax

The query string syntax is passed through directly to the JGI JAMO Search service, which in turn (preumably) passess it straight through to the Elasticsearch back end.



```
    /*
        SearchFilter
        The jgi back end takes a map of either string, integer, or array of integer.
        I don't think the type compiler supports union types, so unspecified it is.
    */
    typedef mapping<string, UnspecifiedObject> SearchFilter;
    typedef mapping<string, string> SearchQuery;

    /*
        search_jgi searches the JGI service for matches against the
        query, which may be a string or an object mapping string->string

        query - 

        Other parameters
        @optional filter 
        @optional limit
        @optional page
        @optional include_private
    */
    typedef structure {
        SearchQuery query;
        SearchFilter filter;
        int limit;
        int page;
        bool include_private;
    } SearchInput;
```