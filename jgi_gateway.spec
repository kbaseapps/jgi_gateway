/*
A KBase module: jgi_gateway
*/

module jgi_gateway {

    /*
        a bool defined as int
    */
    typedef int bool;

    /*
        search_jgi searches the JGI service for matches against the
        search_string

        Other parameters
        @optional limit
        @optional page
    */
    typedef structure {
        string search_string;
        int limit;
        int page;
    } SearchInput;

    typedef mapping<string, string> docdata;
    typedef structure {
       list<docdata> doc_data;
    } SearchResults;


    /*
        The search_jgi function takes a search string and returns a list of
        documents.
    */
    funcdef search_jgi(SearchInput input) returns (SearchResults output) authentication required;

    typedef structure {
       list<string> ids;
    } StageInput;

    typedef mapping<string, string> StagingResults;

    funcdef stage_objects(StageInput input) returns (StagingResults results) authentication required;
};
