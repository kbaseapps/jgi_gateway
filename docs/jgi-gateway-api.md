# JGI Gateway API

## search_jgi

### Input


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