# JGI Search API

This document describes the JGI JAMO Search API

```
client -> jgi-gateway dynamic service -> jgi-search search service
```

This document describes the jgi-search service; see [the JGI Gateway](jgi-gateway-api.md) document for the kbase service.

> See also the JGI documentation locationed within this same directory

## Overview

The JGI Search Service (jgi-search) provides and interface to the JGI Archive and Metadata Organizer (JAMO). jgi-search consists of an api which accepts requests to query an elasticsearch database for JAMO content, and also to transfer JAMO content into the KBase "staging area" file system. The jgi-search database is essentially a mapping of metadata to files, using elasticsearch (at present) as the database and query language, and behind that a file retrieval and transfer system. 

Although jgi-search uses elasticsearch, it does not expose the elasticsearch query syntax.

## API

The jgi-search api is http-based, with json as the content format for both receiving and sending. It is not follow json-rpc or any othe specific protocol. Rather it is simply composed of http post requests which expect json as the request content, and return (mostly) json as the response.

Security is provided by being restricting communication to https and a basic auth credential (secret.)  The basic auth credentials are passed with each request, and are simply known and provided to KBase. The credentials are known to and stored by the kbase dynamic service.

> Is there anything else? IP whitelisting perhaps?

### query

The query endpoint provides all of the search capabilty of the api. It supports free text and by-field queries, using a custom syntax, as well as optional by-field filtering. It supports paging and the inclusion of private data (public is always searched).

A maximum of 10,000 search items may be accessed. The correct number of search results will be reported in the "total" property of the result, but items beyond 10,000 cannot be accessed and will result in an error.

#### URL

POST <endpoint>/query

#### Header

Basic-Auth: <jgi username>:<jgi password>
Content-Type: application/json
Accept: application/json

#### Payload

The body sent in the request is JSON, with the following top level properties:

- query: required: a query string or map of in which the keys are searchable fields, the values are strings in the query syntax (below), and an optional "operator" property specifics the boolean operation on the fiels (or, and, not).

- filter: optional: a map providing a set of field values to be used as a "filter" query. In brief, it is an equivalent but different form of query than the normal query. Described below.

- limit: optional: the number of items to be returned out of the total result set of found items; defaults to 10. Think of this as "page size". Combined with the logic of "page" below, this provides the capability of paged access to a query.

- page: optional: given the total result set, and a "page size", this represents the "page" of results to return; defaults to 0. 

- userid: optional: A string providing the username of the current kbase user; defaults to none. If provided, the search will cover private data owned by the JGI user(s) associated with this KBase user account.


##### query

The ```query``` property is the only required field in the ```/query``` call. It can take the form of a string or an object which provides fields as keys and search values as the string values. A special property "operator" indicates how the one or more keys are combined - "OR", "AND", "NOT". An "OR" is implied if the "operator" property is omitted.

###### query format

> paraphrased from JGI documentation

If the query value is simply a string, it will be used to perform a full text search. (This is the same as the "_all" field described below.) Multiple words in the string can be combined with boolean logic using a single operator. The default operator is OR.

The query string supports the standard Elasticsearch [Simple Query String](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-simple-query-string-query.html) syntax.

In short:

| Operator | Meaning    |
|:--------:|------------|
| +        | signifies AND operation |
| \|        | signifies OR operation |
| -        | negates a single token  |
| "        | wraps a number of tokens to signify a phrase for searching * at the end of a term signifies a prefix query |
| ( and )  | signify precedence |
| ~N       | after a word signifies edit distance (fuzziness) ~N after a phrase signifies slop amount |

In order to search for any of these special characters, they will need to be escaped
Default operator is OR

###### per-field format

The second format for the query property is a one-level object of string values. Each property is either a field query or the boolean operator.

Field queries may include any field found in search documents. The key is the "path" to the key, starting at the ```_xxx``` property (see the result value definition below), with periods separating path elements. The special field ```_all``` includes all fields of the document; a search issued against this field will search all configured fields (effectivelly all the text in the document including numbers converted to strings.) A search of _all is the same as using the query as the sole value of the query property.


The special query property ```operator``` is one of "OR", "AND", "NOT", and indicates the boolean operator to be applied to all of the provided fields.

###### Examples

```json
{
    "file_type": "fastq | fasta",
    "_all": "strep*",
    "operator": "AND"
}
```

This will search for all records which include words starting with "strep" (the "*" wildcard matches anything following "strep"), and have the file_type field set to either "fastq" or "fasta".


##### filter

The filter property is simliar to query, but provides exact matches against single values or value lists, utilizes numeric values in some cases, and is more performant. Filters are a feature of Elasticsearch queries.

The filter is a simple, one-level object similar to the query property. Some fields are specially handled and support multiple formats, including integer. The "operator" property specifies the boolean operation applied to all of the filter properties, and defaults to "OR".

The following fiels are specially handled:

- proposal_id
- project_id
- project_title
- pi_name
- project_date

They would normally be accessed by their property path, but they are available at the top level. In addition, they support data types beyond string. All other search objects are filtered by an exact string match.

> TODO: does this imply that only strings are supported?

```proposal_id``` and ```project_id``` are both integer values. The value for their filter property may take any of the following forms:
- a string containing an integer
- a string containgin 2 or more integers separated by a comma
- a single integer (?)
- an array of integers

For the multiple-value forms, the values are "or"ed together; the field will match on any of the values included in the list.

E.g.

```json
{
    "query": {"_all": "*"},
    "filter": {"project_id": 456}
}
```

```json
{
    "query": {"_all": "*"},
    "filter": {"project_id": [123, 456]}
}
```

```json
{
    "query": {"_all": "*"},
    "filter": {"project_id": "123,456"}
}
```

```json
{
    "query": {"_all": "*"},
    "filter": {"project_id": "123"}
}
```

The ```project_date``` is a date value.

> TODO: the usage of date is not documented by JGI; we might assume it is an ISO or US date format.

The ```pi_name``` and ```project_title``` are specially handled as well

> TODO: the jgi doc mentions them, but not anything about how they are special. Well, they are hoisted to the top level, but it isnt' clear what fields they correspond to (are they coalesced from more than one?) or what processing might be special (e.g. neither pi name nor project title are too useful in exact searches)



##### limit

The optional limit property is an integer specifing the maximum number of items to return from a query. It must be 1 or greater and less than 10,000 (the maximum number of search results that may be accessed.)

It defaults to 10.

This value, together with the page property described below, provide "paged" search. If you think of the size as the "page size" and the "page" parameter described below as the nth page to return.

##### page

The optional page property is an integer specifying the nth "page" of results to return. It is an integer between 0 and 10,000. It is therefore a 0-based page numbering scheme.

It defaults to 0.

Put another way, it specifies that the first result item returned is page * limit.

> What is the behavior when requesting a page beyond that which exists in the results?

In practice, since upon an initial query it is unknown how may items exist, the page is set to 0, and the calling client is in charge of calculating the effective maximum page based on the current limit and the total number of search items.