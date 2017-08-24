package us.kbase.jgigatewayeap;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.Tuple2;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: jgi_gateway_eap</p>
 * <pre>
 * A KBase module: jgi_gateway_eap
 * </pre>
 */
public class JgiGatewayEapClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public JgiGatewayEapClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public JgiGatewayEapClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public JgiGatewayEapClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public JgiGatewayEapClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: search_jgi</p>
     * <pre>
     * The search_jgi function takes a search string and returns a list of
     * documents.
     * </pre>
     * @param   input   instance of type {@link us.kbase.jgigatewayeap.SearchInput SearchInput}
     * @return   multiple set: (1) parameter "result" of type {@link us.kbase.jgigatewayeap.SearchResult SearchResult}, (2) parameter "stats" of type {@link us.kbase.jgigatewayeap.CallStats CallStats}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<SearchResult, CallStats> searchJgi(SearchInput input, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(input);
        TypeReference<Tuple2<SearchResult, CallStats>> retType = new TypeReference<Tuple2<SearchResult, CallStats>>() {};
        Tuple2<SearchResult, CallStats> res = caller.jsonrpcCall("jgi_gateway_eap.search_jgi", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: stage_objects</p>
     * <pre>
     * </pre>
     * @param   input   instance of type {@link us.kbase.jgigatewayeap.StageInput StageInput}
     * @return   multiple set: (1) parameter "result" of original type "StagingResult" (StagingResult returns a map entry for each id submitted in the stage_objects request. The map key is the _id property returned in a SearchResult item (not described here but probably should be), the value is a string describing the result of the staging request. At time of writing, the value is always "staging" since the request to the jgi gateway jgi service and the call to stage_objects in the jgi gateway kbase service are in different processes.) &rarr; mapping from String to String, (2) parameter "stats" of type {@link us.kbase.jgigatewayeap.CallStats CallStats}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<Map<String,String>, CallStats> stageObjects(StageInput input, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(input);
        TypeReference<Tuple2<Map<String,String>, CallStats>> retType = new TypeReference<Tuple2<Map<String,String>, CallStats>>() {};
        Tuple2<Map<String,String>, CallStats> res = caller.jsonrpcCall("jgi_gateway_eap.stage_objects", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: stage_status</p>
     * <pre>
     * Fetch the current status of the given staging fetch request as 
     * identified by its job id
     * </pre>
     * @param   jobId   instance of String
     * @return   multiple set: (1) parameter "result" of type {@link us.kbase.jgigatewayeap.StagingStatusResult StagingStatusResult}, (2) parameter "stats" of type {@link us.kbase.jgigatewayeap.CallStats CallStats}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<StagingStatusResult, CallStats> stageStatus(String jobId, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(jobId);
        TypeReference<Tuple2<StagingStatusResult, CallStats>> retType = new TypeReference<Tuple2<StagingStatusResult, CallStats>>() {};
        Tuple2<StagingStatusResult, CallStats> res = caller.jsonrpcCall("jgi_gateway_eap.stage_status", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res;
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("jgi_gateway_eap.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
