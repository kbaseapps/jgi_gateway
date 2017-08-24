package jgi_gateway_eap::jgi_gateway_eapClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

jgi_gateway_eap::jgi_gateway_eapClient

=head1 DESCRIPTION


A KBase module: jgi_gateway_eap


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => jgi_gateway_eap::jgi_gateway_eapClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 search_jgi

  $result, $stats = $obj->search_jgi($input)

=over 4

=item Parameter and return types

=begin html

<pre>
$input is a jgi_gateway_eap.SearchInput
$result is a jgi_gateway_eap.SearchResult
$stats is a jgi_gateway_eap.CallStats
SearchInput is a reference to a hash where the following keys are defined:
	search_string has a value which is a string
	limit has a value which is an int
	page has a value which is an int
SearchResult is a reference to a hash where the following keys are defined:
	search_result has a value which is a jgi_gateway_eap.SearchQueryResult
SearchQueryResult is a reference to a list where each element is an UnspecifiedObject, which can hold any non-null object
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int

</pre>

=end html

=begin text

$input is a jgi_gateway_eap.SearchInput
$result is a jgi_gateway_eap.SearchResult
$stats is a jgi_gateway_eap.CallStats
SearchInput is a reference to a hash where the following keys are defined:
	search_string has a value which is a string
	limit has a value which is an int
	page has a value which is an int
SearchResult is a reference to a hash where the following keys are defined:
	search_result has a value which is a jgi_gateway_eap.SearchQueryResult
SearchQueryResult is a reference to a list where each element is an UnspecifiedObject, which can hold any non-null object
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int


=end text

=item Description

The search_jgi function takes a search string and returns a list of
documents.

=back

=cut

 sub search_jgi
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function search_jgi (received $n, expecting 1)");
    }
    {
	my($input) = @args;

	my @_bad_arguments;
        (ref($input) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"input\" (value was \"$input\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to search_jgi:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'search_jgi');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "jgi_gateway_eap.search_jgi",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'search_jgi',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method search_jgi",
					    status_line => $self->{client}->status_line,
					    method_name => 'search_jgi',
				       );
    }
}
 


=head2 stage_objects

  $result, $stats = $obj->stage_objects($input)

=over 4

=item Parameter and return types

=begin html

<pre>
$input is a jgi_gateway_eap.StageInput
$result is a jgi_gateway_eap.StagingResult
$stats is a jgi_gateway_eap.CallStats
StageInput is a reference to a hash where the following keys are defined:
	ids has a value which is a reference to a list where each element is a string
StagingResult is a reference to a hash where the key is a string and the value is a string
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int

</pre>

=end html

=begin text

$input is a jgi_gateway_eap.StageInput
$result is a jgi_gateway_eap.StagingResult
$stats is a jgi_gateway_eap.CallStats
StageInput is a reference to a hash where the following keys are defined:
	ids has a value which is a reference to a list where each element is a string
StagingResult is a reference to a hash where the key is a string and the value is a string
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int


=end text

=item Description



=back

=cut

 sub stage_objects
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function stage_objects (received $n, expecting 1)");
    }
    {
	my($input) = @args;

	my @_bad_arguments;
        (ref($input) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"input\" (value was \"$input\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to stage_objects:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'stage_objects');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "jgi_gateway_eap.stage_objects",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'stage_objects',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method stage_objects",
					    status_line => $self->{client}->status_line,
					    method_name => 'stage_objects',
				       );
    }
}
 


=head2 stage_status

  $result, $stats = $obj->stage_status($job_id)

=over 4

=item Parameter and return types

=begin html

<pre>
$job_id is a string
$result is a jgi_gateway_eap.StagingStatusResult
$stats is a jgi_gateway_eap.CallStats
StagingStatusResult is a reference to a hash where the following keys are defined:
	message has a value which is a string
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int

</pre>

=end html

=begin text

$job_id is a string
$result is a jgi_gateway_eap.StagingStatusResult
$stats is a jgi_gateway_eap.CallStats
StagingStatusResult is a reference to a hash where the following keys are defined:
	message has a value which is a string
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int


=end text

=item Description

Fetch the current status of the given staging fetch request as 
identified by its job id

=back

=cut

 sub stage_status
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function stage_status (received $n, expecting 1)");
    }
    {
	my($job_id) = @args;

	my @_bad_arguments;
        (!ref($job_id)) or push(@_bad_arguments, "Invalid type for argument 1 \"job_id\" (value was \"$job_id\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to stage_status:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'stage_status');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "jgi_gateway_eap.stage_status",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'stage_status',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method stage_status",
					    status_line => $self->{client}->status_line,
					    method_name => 'stage_status',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "jgi_gateway_eap.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "jgi_gateway_eap.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'stage_status',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method stage_status",
            status_line => $self->{client}->status_line,
            method_name => 'stage_status',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for jgi_gateway_eap::jgi_gateway_eapClient\n";
    }
    if ($sMajor == 0) {
        warn "jgi_gateway_eap::jgi_gateway_eapClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 bool

=over 4



=item Description

a bool defined as int


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 CallStats

=over 4



=item Description

Call performance measurement


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
request_elapsed_time has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
request_elapsed_time has a value which is an int


=end text

=back



=head2 SearchInput

=over 4



=item Description

search_jgi searches the JGI service for matches against the
search_string

Other parameters
@optional limit
@optional page


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
search_string has a value which is a string
limit has a value which is an int
page has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
search_string has a value which is a string
limit has a value which is an int
page has a value which is an int


=end text

=back



=head2 SearchQueryResult

=over 4



=item Description

typedef mapping<string, string> docdata;


=item Definition

=begin html

<pre>
a reference to a list where each element is an UnspecifiedObject, which can hold any non-null object
</pre>

=end html

=begin text

a reference to a list where each element is an UnspecifiedObject, which can hold any non-null object

=end text

=back



=head2 SearchResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
search_result has a value which is a jgi_gateway_eap.SearchQueryResult

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
search_result has a value which is a jgi_gateway_eap.SearchQueryResult


=end text

=back



=head2 StageInput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ids has a value which is a reference to a list where each element is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ids has a value which is a reference to a list where each element is a string


=end text

=back



=head2 StagingResult

=over 4



=item Description

StagingResult returns a map entry for each id submitted in the stage_objects request.
The map key is the _id property returned in a SearchResult item (not described here but probably 
should be), the value is a string describing the result of the staging request.
At time of writing, the value is always "staging" since the request to the jgi gateway jgi service
and the call to stage_objects in the jgi gateway kbase service are in different processes.


=item Definition

=begin html

<pre>
a reference to a hash where the key is a string and the value is a string
</pre>

=end html

=begin text

a reference to a hash where the key is a string and the value is a string

=end text

=back



=head2 StagingStatusResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
message has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
message has a value which is a string


=end text

=back



=cut

package jgi_gateway_eap::jgi_gateway_eapClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
