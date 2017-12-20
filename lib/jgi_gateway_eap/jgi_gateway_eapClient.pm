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




=head2 search

  $result, $error, $stats = $obj->search($parameter)

=over 4

=item Parameter and return types

=begin html

<pre>
$parameter is a jgi_gateway_eap.SearchInput
$result is a jgi_gateway_eap.SearchResult
$error is a jgi_gateway_eap.Error
$stats is a jgi_gateway_eap.CallStats
SearchInput is a reference to a hash where the following keys are defined:
	query has a value which is a jgi_gateway_eap.SearchQuery
	filter has a value which is a jgi_gateway_eap.SearchFilter
	sort has a value which is a reference to a list where each element is a jgi_gateway_eap.SortSpec
	limit has a value which is an int
	page has a value which is an int
	include_private has a value which is a jgi_gateway_eap.bool
SearchQuery is a reference to a hash where the key is a string and the value is a string
SearchFilter is a reference to a hash where the key is a string and the value is an UnspecifiedObject, which can hold any non-null object
SortSpec is a reference to a hash where the following keys are defined:
	field has a value which is a string
	descending has a value which is an int
bool is an int
SearchResult is a reference to a hash where the following keys are defined:
	search_result has a value which is a jgi_gateway_eap.SearchQueryResult
SearchQueryResult is a reference to a hash where the following keys are defined:
	hits has a value which is a reference to a list where each element is a jgi_gateway_eap.SearchResultItem
	total has a value which is an int
SearchResultItem is a reference to a hash where the following keys are defined:
	source has a value which is a jgi_gateway_eap.SearchDocument
	index has a value which is a string
	score has a value which is a string
	id has a value which is a string
SearchDocument is an UnspecifiedObject, which can hold any non-null object
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int

</pre>

=end html

=begin text

$parameter is a jgi_gateway_eap.SearchInput
$result is a jgi_gateway_eap.SearchResult
$error is a jgi_gateway_eap.Error
$stats is a jgi_gateway_eap.CallStats
SearchInput is a reference to a hash where the following keys are defined:
	query has a value which is a jgi_gateway_eap.SearchQuery
	filter has a value which is a jgi_gateway_eap.SearchFilter
	sort has a value which is a reference to a list where each element is a jgi_gateway_eap.SortSpec
	limit has a value which is an int
	page has a value which is an int
	include_private has a value which is a jgi_gateway_eap.bool
SearchQuery is a reference to a hash where the key is a string and the value is a string
SearchFilter is a reference to a hash where the key is a string and the value is an UnspecifiedObject, which can hold any non-null object
SortSpec is a reference to a hash where the following keys are defined:
	field has a value which is a string
	descending has a value which is an int
bool is an int
SearchResult is a reference to a hash where the following keys are defined:
	search_result has a value which is a jgi_gateway_eap.SearchQueryResult
SearchQueryResult is a reference to a hash where the following keys are defined:
	hits has a value which is a reference to a list where each element is a jgi_gateway_eap.SearchResultItem
	total has a value which is an int
SearchResultItem is a reference to a hash where the following keys are defined:
	source has a value which is a jgi_gateway_eap.SearchDocument
	index has a value which is a string
	score has a value which is a string
	id has a value which is a string
SearchDocument is an UnspecifiedObject, which can hold any non-null object
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int


=end text

=item Description

The search function takes a search structure and returns a list of
documents.

=back

=cut

 sub search
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function search (received $n, expecting 1)");
    }
    {
	my($parameter) = @args;

	my @_bad_arguments;
        (ref($parameter) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"parameter\" (value was \"$parameter\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to search:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'search');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "jgi_gateway_eap.search",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'search',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method search",
					    status_line => $self->{client}->status_line,
					    method_name => 'search',
				       );
    }
}
 


=head2 stage

  $result, $error, $stats = $obj->stage($parameter)

=over 4

=item Parameter and return types

=begin html

<pre>
$parameter is a jgi_gateway_eap.StageInput
$result is a jgi_gateway_eap.StagingResult
$error is a jgi_gateway_eap.Error
$stats is a jgi_gateway_eap.CallStats
StageInput is a reference to a hash where the following keys are defined:
	file has a value which is a jgi_gateway_eap.StageRequest
StageRequest is a reference to a hash where the following keys are defined:
	id has a value which is a string
	filename has a value which is a string
	username has a value which is a string
StagingResult is a reference to a hash where the following keys are defined:
	job_id has a value which is a string
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int

</pre>

=end html

=begin text

$parameter is a jgi_gateway_eap.StageInput
$result is a jgi_gateway_eap.StagingResult
$error is a jgi_gateway_eap.Error
$stats is a jgi_gateway_eap.CallStats
StageInput is a reference to a hash where the following keys are defined:
	file has a value which is a jgi_gateway_eap.StageRequest
StageRequest is a reference to a hash where the following keys are defined:
	id has a value which is a string
	filename has a value which is a string
	username has a value which is a string
StagingResult is a reference to a hash where the following keys are defined:
	job_id has a value which is a string
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int


=end text

=item Description



=back

=cut

 sub stage
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function stage (received $n, expecting 1)");
    }
    {
	my($parameter) = @args;

	my @_bad_arguments;
        (ref($parameter) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"parameter\" (value was \"$parameter\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to stage:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'stage');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "jgi_gateway_eap.stage",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'stage',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method stage",
					    status_line => $self->{client}->status_line,
					    method_name => 'stage',
				       );
    }
}
 


=head2 stage_status

  $result, $error, $stats = $obj->stage_status($parameter)

=over 4

=item Parameter and return types

=begin html

<pre>
$parameter is a jgi_gateway_eap.StagingStatusInput
$result is a jgi_gateway_eap.StagingStatusResult
$error is a jgi_gateway_eap.Error
$stats is a jgi_gateway_eap.CallStats
StagingStatusInput is a reference to a hash where the following keys are defined:
	job_id has a value which is a string
StagingStatusResult is a reference to a hash where the following keys are defined:
	message has a value which is a string
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int

</pre>

=end html

=begin text

$parameter is a jgi_gateway_eap.StagingStatusInput
$result is a jgi_gateway_eap.StagingStatusResult
$error is a jgi_gateway_eap.Error
$stats is a jgi_gateway_eap.CallStats
StagingStatusInput is a reference to a hash where the following keys are defined:
	job_id has a value which is a string
StagingStatusResult is a reference to a hash where the following keys are defined:
	message has a value which is a string
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
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
	my($parameter) = @args;

	my @_bad_arguments;
        (ref($parameter) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"parameter\" (value was \"$parameter\")");
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
 


=head2 staging_jobs

  $result, $error, $stats = $obj->staging_jobs($parameter)

=over 4

=item Parameter and return types

=begin html

<pre>
$parameter is a jgi_gateway_eap.StagingJobsInput
$result is a jgi_gateway_eap.StagingJobsResult
$error is a jgi_gateway_eap.Error
$stats is a jgi_gateway_eap.CallStats
StagingJobsInput is a reference to a hash where the following keys are defined:
	filter has a value which is a jgi_gateway_eap.StagingJobsFilter
	range has a value which is a jgi_gateway_eap.StagingJobsRange
	sort has a value which is a reference to a list where each element is a jgi_gateway_eap.SortSpec
StagingJobsFilter is a reference to a hash where the following keys are defined:
	created_from has a value which is a jgi_gateway_eap.timestamp
	created_to has a value which is a jgi_gateway_eap.timestamp
	updated_from has a value which is a jgi_gateway_eap.timestamp
	updated_to has a value which is a jgi_gateway_eap.timestamp
	status has a value which is a string
	jamo_id has a value which is a string
	job_ids has a value which is a reference to a list where each element is a string
	filename has a value which is a string
timestamp is an int
StagingJobsRange is a reference to a hash where the following keys are defined:
	start has a value which is an int
	limit has a value which is an int
SortSpec is a reference to a hash where the following keys are defined:
	field has a value which is a string
	descending has a value which is an int
StagingJobsResult is a reference to a hash where the following keys are defined:
	staging_jobs has a value which is a reference to a list where each element is a jgi_gateway_eap.StagingJob
	total_matched has a value which is an int
	total_jobs has a value which is an int
StagingJob is a reference to a hash where the following keys are defined:
	jamo_id has a value which is a string
	filename has a value which is a string
	username has a value which is a string
	job_id has a value which is a string
	status_code has a value which is a string
	status_raw has a value which is a string
	created has a value which is a jgi_gateway_eap.timestamp
	updated has a value which is a jgi_gateway_eap.timestamp
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int

</pre>

=end html

=begin text

$parameter is a jgi_gateway_eap.StagingJobsInput
$result is a jgi_gateway_eap.StagingJobsResult
$error is a jgi_gateway_eap.Error
$stats is a jgi_gateway_eap.CallStats
StagingJobsInput is a reference to a hash where the following keys are defined:
	filter has a value which is a jgi_gateway_eap.StagingJobsFilter
	range has a value which is a jgi_gateway_eap.StagingJobsRange
	sort has a value which is a reference to a list where each element is a jgi_gateway_eap.SortSpec
StagingJobsFilter is a reference to a hash where the following keys are defined:
	created_from has a value which is a jgi_gateway_eap.timestamp
	created_to has a value which is a jgi_gateway_eap.timestamp
	updated_from has a value which is a jgi_gateway_eap.timestamp
	updated_to has a value which is a jgi_gateway_eap.timestamp
	status has a value which is a string
	jamo_id has a value which is a string
	job_ids has a value which is a reference to a list where each element is a string
	filename has a value which is a string
timestamp is an int
StagingJobsRange is a reference to a hash where the following keys are defined:
	start has a value which is an int
	limit has a value which is an int
SortSpec is a reference to a hash where the following keys are defined:
	field has a value which is a string
	descending has a value which is an int
StagingJobsResult is a reference to a hash where the following keys are defined:
	staging_jobs has a value which is a reference to a list where each element is a jgi_gateway_eap.StagingJob
	total_matched has a value which is an int
	total_jobs has a value which is an int
StagingJob is a reference to a hash where the following keys are defined:
	jamo_id has a value which is a string
	filename has a value which is a string
	username has a value which is a string
	job_id has a value which is a string
	status_code has a value which is a string
	status_raw has a value which is a string
	created has a value which is a jgi_gateway_eap.timestamp
	updated has a value which is a jgi_gateway_eap.timestamp
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
CallStats is a reference to a hash where the following keys are defined:
	request_elapsed_time has a value which is an int


=end text

=item Description

Fetch all file staging jobs for the current user

=back

=cut

 sub staging_jobs
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function staging_jobs (received $n, expecting 1)");
    }
    {
	my($parameter) = @args;

	my @_bad_arguments;
        (ref($parameter) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"parameter\" (value was \"$parameter\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to staging_jobs:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'staging_jobs');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "jgi_gateway_eap.staging_jobs",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'staging_jobs',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method staging_jobs",
					    status_line => $self->{client}->status_line,
					    method_name => 'staging_jobs',
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
                method_name => 'staging_jobs',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method staging_jobs",
            status_line => $self->{client}->status_line,
            method_name => 'staging_jobs',
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



=head2 Error

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
message has a value which is a string
type has a value which is a string
code has a value which is a string
info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
message has a value which is a string
type has a value which is a string
code has a value which is a string
info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=back



=head2 SearchFilter

=over 4



=item Description

SearchFilter
The jgi back end takes a map of either string, integer, or array of integer.
I don't think the type compiler supports union types, so unspecified it is.


=item Definition

=begin html

<pre>
a reference to a hash where the key is a string and the value is an UnspecifiedObject, which can hold any non-null object
</pre>

=end html

=begin text

a reference to a hash where the key is a string and the value is an UnspecifiedObject, which can hold any non-null object

=end text

=back



=head2 SearchQuery

=over 4



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



=head2 SortSpec

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
field has a value which is a string
descending has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
field has a value which is a string
descending has a value which is an int


=end text

=back



=head2 SearchInput

=over 4



=item Description

search searches the JGI service for matches against the
query, which may be a string or an object mapping string->string

query - 

Other parameters
@optional filter 
@optional limit
@optional page
@optional include_private


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
query has a value which is a jgi_gateway_eap.SearchQuery
filter has a value which is a jgi_gateway_eap.SearchFilter
sort has a value which is a reference to a list where each element is a jgi_gateway_eap.SortSpec
limit has a value which is an int
page has a value which is an int
include_private has a value which is a jgi_gateway_eap.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
query has a value which is a jgi_gateway_eap.SearchQuery
filter has a value which is a jgi_gateway_eap.SearchFilter
sort has a value which is a reference to a list where each element is a jgi_gateway_eap.SortSpec
limit has a value which is an int
page has a value which is an int
include_private has a value which is a jgi_gateway_eap.bool


=end text

=back



=head2 SearchDocument

=over 4



=item Description

SearchDocument
The source document for the search; it is both the data obtained by the
search as well as the source of the index. 
It is the entire metadata JAMO record.


=item Definition

=begin html

<pre>
an UnspecifiedObject, which can hold any non-null object
</pre>

=end html

=begin text

an UnspecifiedObject, which can hold any non-null object

=end text

=back



=head2 SearchResultItem

=over 4



=item Description

SearchResult
Represents a single search result item


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
source has a value which is a jgi_gateway_eap.SearchDocument
index has a value which is a string
score has a value which is a string
id has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
source has a value which is a jgi_gateway_eap.SearchDocument
index has a value which is a string
score has a value which is a string
id has a value which is a string


=end text

=back



=head2 SearchQueryResult

=over 4



=item Description

SearchQueryResult
The top level search object returned from the query.
Note that this structure closely parallels that returned by the jgi search service.
The only functional difference is that some field names which were prefixed by 
underscore are known by their unprefixed selfs.
hits  - a list of the actual search result documents and statsitics returned;;
        note that this represents the window of search results defined by
        the limit input property.
total - the total number of items matched by the search; not the same as the 
       items actually returned;


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
hits has a value which is a reference to a list where each element is a jgi_gateway_eap.SearchResultItem
total has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
hits has a value which is a reference to a list where each element is a jgi_gateway_eap.SearchResultItem
total has a value which is an int


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



=head2 StageRequest

=over 4



=item Description

STAGE


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
id has a value which is a string
filename has a value which is a string
username has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
id has a value which is a string
filename has a value which is a string
username has a value which is a string


=end text

=back



=head2 StageInput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
file has a value which is a jgi_gateway_eap.StageRequest

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
file has a value which is a jgi_gateway_eap.StageRequest


=end text

=back



=head2 StagingResult

=over 4



=item Description

StagingResult returns a map entry for each id submitted in the stage request.
The map key is the _id property returned in a SearchResult item (not described here but probably 
should be), the value is a string describing the result of the staging request.
At time of writing, the value is always "staging" since the request to the jgi gateway jgi service
and the call to stage in the jgi gateway kbase service are in different processes.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
job_id has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
job_id has a value which is a string


=end text

=back



=head2 StagingStatusInput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
job_id has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
job_id has a value which is a string


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



=head2 timestamp

=over 4



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



=head2 StagingJob

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
jamo_id has a value which is a string
filename has a value which is a string
username has a value which is a string
job_id has a value which is a string
status_code has a value which is a string
status_raw has a value which is a string
created has a value which is a jgi_gateway_eap.timestamp
updated has a value which is a jgi_gateway_eap.timestamp

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
jamo_id has a value which is a string
filename has a value which is a string
username has a value which is a string
job_id has a value which is a string
status_code has a value which is a string
status_raw has a value which is a string
created has a value which is a jgi_gateway_eap.timestamp
updated has a value which is a jgi_gateway_eap.timestamp


=end text

=back



=head2 StagingJobsFilter

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
created_from has a value which is a jgi_gateway_eap.timestamp
created_to has a value which is a jgi_gateway_eap.timestamp
updated_from has a value which is a jgi_gateway_eap.timestamp
updated_to has a value which is a jgi_gateway_eap.timestamp
status has a value which is a string
jamo_id has a value which is a string
job_ids has a value which is a reference to a list where each element is a string
filename has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
created_from has a value which is a jgi_gateway_eap.timestamp
created_to has a value which is a jgi_gateway_eap.timestamp
updated_from has a value which is a jgi_gateway_eap.timestamp
updated_to has a value which is a jgi_gateway_eap.timestamp
status has a value which is a string
jamo_id has a value which is a string
job_ids has a value which is a reference to a list where each element is a string
filename has a value which is a string


=end text

=back



=head2 StagingJobsRange

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
start has a value which is an int
limit has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
start has a value which is an int
limit has a value which is an int


=end text

=back



=head2 StagingJobsInput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
filter has a value which is a jgi_gateway_eap.StagingJobsFilter
range has a value which is a jgi_gateway_eap.StagingJobsRange
sort has a value which is a reference to a list where each element is a jgi_gateway_eap.SortSpec

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
filter has a value which is a jgi_gateway_eap.StagingJobsFilter
range has a value which is a jgi_gateway_eap.StagingJobsRange
sort has a value which is a reference to a list where each element is a jgi_gateway_eap.SortSpec


=end text

=back



=head2 StagingJobsResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
staging_jobs has a value which is a reference to a list where each element is a jgi_gateway_eap.StagingJob
total_matched has a value which is an int
total_jobs has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
staging_jobs has a value which is a reference to a list where each element is a jgi_gateway_eap.StagingJob
total_matched has a value which is an int
total_jobs has a value which is an int


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
