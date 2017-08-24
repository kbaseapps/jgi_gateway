/*
A KBase module: jgi_gateway_eap
*/

module jgi_gateway_eap {

    /*
        a bool defined as int
    */
    typedef int bool;

    /*
        Call performance measurement
    */
    typedef structure {        
        int request_elapsed_time;
    } CallStats;

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


    /*
      SearchQueryResult holds the actual json returned by the 
      backend search api.
      TODO: the data returned is not really a string,string map, although
      python doesn't care.
    */
    /* typedef mapping<string, string> docdata; */
    typedef list<UnspecifiedObject> SearchQueryResult;

    typedef structure {
       SearchQueryResult search_result;
    } SearchResult;


    /*
        The search_jgi function takes a search string and returns a list of
        documents.
    */
    funcdef search_jgi(SearchInput input) 
            returns (SearchResult result, CallStats stats) 
            authentication required;

    typedef structure {
       list<string> ids;
    } StageInput;

    /*
        StagingResult returns a map entry for each id submitted in the stage_objects request.
        The map key is the _id property returned in a SearchResult item (not described here but probably 
        should be), the value is a string describing the result of the staging request.
        At time of writing, the value is always "staging" since the request to the jgi gateway jgi service
        and the call to stage_objects in the jgi gateway kbase service are in different processes.
    */
    typedef mapping<string, string> StagingResult;

    funcdef stage_objects(StageInput input) 
            returns (StagingResult result, CallStats stats) 
            authentication required;

   

    typedef structure {
        string message;
    } StagingStatusResult;

    /* Fetch the current status of the given staging fetch request as 
       identified by its job id */
    funcdef stage_status(string job_id) 
            returns (StagingStatusResult result, CallStats stats) 
            authentication required;

};
