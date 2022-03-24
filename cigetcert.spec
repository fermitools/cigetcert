Summary: Get an X.509 certificate with SAML ECP and store proxies
Name: cigetcert
Version: 1.19
Release: 2%{?dist}
License: BSD
Group: Applications/System
URL: http://redmine.fnal.gov/projects/fermitools/wiki/cigetcert
# download with:
# $ curl -o cigetcert-%{version}.tar.gz \
#    https://codeload.github.com/fermitools/cigetcert/tar.gz/%{version}
Source0: %{name}-%{version}.tar.gz
%if %{?rhel}%{!?rhel:8} < 8
%define _python python
Requires: m2crypto
Requires: pyOpenSSL
%else
%define _python python3
%define _pycompflag -b
Requires: python3-m2crypto
Requires: python3-pyOpenSSL
%endif
Requires: %{_python}
Requires: %{_python}-lxml
Requires: %{_python}-kerberos
BuildRequires: %{_python}

BuildArch: noarch

%description
cigetcert gets an X.509 certificate from a SAML 2.0 Service Provider
(SP) such as CILogon using the Enhanced Client and Proxy (ECP)
profile. Optionally it can also get a grid proxy certificate and/or
transfer the proxy to MyProxy. It was developed for the Fermilab
Distributed Computing Access with Federated Identities (DCAFI) project
but is intended to be usable by other projects.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/man/man1
sed 's,/usr/bin/python,/usr/bin/%{_python},' %{name}.sh >$RPM_BUILD_ROOT%{_bindir}/%{name}
chmod 755 $RPM_BUILD_ROOT%{_bindir}/%{name}
sed 's,/usr/bin/python,/usr/bin/%{_python},' %{name} >$RPM_BUILD_ROOT%{_libexecdir}/%{name}/%{name}.py
chmod 644 $RPM_BUILD_ROOT%{_libexecdir}/%{name}/%{name}.py
%{_python} -Em compileall %{?_pycompflag} -d %{_libexecdir}/%{name} $RPM_BUILD_ROOT%{_libexecdir}/%{name}
gzip -c %{name}.1 >$RPM_BUILD_ROOT%{_datadir}/man/man1/%{name}.1.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/man/man1/%{name}*


%changelog
#- Add make sources target for koji build
#- Support port numbers in https urls
#- Return all received cookies in the final getcert step

* Wed Feb 26 2020 Dave Dykstra <dwd@fnal.gov> 1.19-2
- Use python3 on rhel8.
- Remove support for rhel5.

* Sat Jul 20 2019 Dave Dykstra <dwd@fnal.gov> 1.19-1
- Add setup.py for making a standard python installation
- Use ssl.get_default_verify_paths() to find default CA paths, when possible
- Make --listinstitutions compatible with python3

* Wed Oct 10 2018 Dave Dykstra <dwd@fnal.gov> 1.18-1
- Make source code completely compatible with python3
- Fix check for more than 5 proxy levels to apply when verbose option
  is not set

* Thu Sep 27 2018 Dave Dykstra <dwd@fnal.gov> 1.17-1
- Make source code partially compatible with python3.

* Fri Mar 03 2017 Dave Dykstra <dwd@fnal.gov> 1.16-2
- In /usr/bin/cigetcert, invoke python with the '-E' option to avoid
  variables like PYTHONHOME.

* Tue Oct 18 2016 Dave Dykstra <dwd@fnal.gov> 1.16-1
- Fix typo in the variable name added in the last version.  This was
  not noticed because it was caught in an exception and caused it to
  always behave as if a previous proxy stored in myproxy could not be
  used.

* Mon Oct 17 2016 Dave Dykstra <dwd@fnal.gov> 1.15-1
- Fix bug that caused the proxy to be stored into MyProxy under the DN
  of a previous certificate (if it existed but could not be reused)
  rather than the newly generated one.

* Tue Oct 11 2016 Dave Dykstra <dwd@fnal.gov> 1.14-1
- Limit the number of proxy levels stripped off of %certsubject to 5.
  This is to catch programming errors where people call voms-proxy-init
  -noregen after every call to cigetcert, even when cigetcert determines
  that the previous proxy can be reused.

* Mon Oct 10 2016 Dave Dykstra <dwd@fnal.gov> 1.13-1
- Choose a prefix for the temp output file in the same directory as the
  output file to avoid renaming across filesystems.

* Thu Oct 06 2016 Dave Dykstra <dwd@fnal.gov> 1.12-1
- Fix bug introduced in 1.11-1 that caused too-long certificates to
  be stored on local disk.

* Thu Sep 29 2016 Dave Dykstra <dwd@fnal.gov> 1.11-1
- If the requested --hours is fractional, round the hours of the
  original certificate up to the next whole number rather than down.
  In this case generate a proxy with the requested fractional hours.

* Wed Sep 28 2016 Dave Dykstra <dwd@fnal.gov> 1.10-1
- Change default --minhours value from 12 to 1.
- If the formula calculating the remaining hours in the myproxy cert
    (%hours - %proxyhours - %minhours) comes out to a value lower
    than %minhours, set it to %minhours

* Thu Sep 22 2016 Dave Dykstra <dwd@fnal.gov> 1.9-1
- Add support for $X509_USER_PROXY as the default value of --out.

* Fri Sep 16 2016 Dave Dykstra <dwd@fnal.gov> 1.8-1
- Allow a previous output file to have additional proxy layers added
  on to it when checking to see if it is still valid.  That is, strip
  off any number of /CN=[0-9]+ or /CN=proxy patterns appended to the
  certificate subject.  In particular this is useful for when someone
  does voms-proxy-init -noregen after a previous run of cigetcert.

* Wed Sep 14 2016 Dave Dykstra <dwd@fnal.gov> 1.7-1
- Fix man page description of --idplisturl
- Do many changes in response to a code review:
  - change default python to the system python in /usr/bin
  - always cleanly shutdown SSL connections to avoid truncation attacks
  - support all TLS versions, not just v1.0
  - disable the possibility of SSL compression to avoid CRIME attack
  - disable SSL ciphers known to be insecure
  - document the fact that CRLs are not actually checked (this is deemed
    to be an acceptable risk)
  - set a timeout on SSL connections to 15 seconds
  - change the message digest on proxies from sha1 to sha256
  - sanitize user input sent directly to myproxy (that is, the username)
  - change maximum proxy duration to a million seconds (277 hours) and
    maximum certificate duration to 10000 hours, leaving the defaults
    as they were
  - disable support for http:// URLs; everything has to be https:// (or
    in some cases file://)
  - use effective uid rather than real uid for the %uid macro
  - use mkstemp() to create the output in a temporary file, in order to
    avoid race conditions where another process could be reading the
    file as cigetcert creates it
  - catch any errors writing the output file to avoid a stack trace
  - add some explanatory comments to the source code
- Add support for Debian
  - Allow alternate default cafile of /etc/ssl/certs/ca-certificates.crt
  - Only use SSL.Connection.settimeout if it is present

* Tue Jul 26 2016 Dave Dykstra <dwd@fnal.gov> 1.6-1
- Add support for $X509_CERT_DIR as the default directory for finding
  CA certs and CRLs.
- Use the time from the underlying certificate for the "Not Before" time
  in proxies rather than the current time.  It is typically 5 minutes
  in the past, which helps with client machines that have clock skew
  up to that far in the future.

* Wed Jul 20 2016 Dave Dykstra <dwd@fnal.gov> 1.5-1
- Make failure to read myproxy into a reuse failure instead of a fatal
  error, because it can be caused by an attempt to use an invalid
  existing proxy such as a non-rfc VOMS proxy.

* Wed Jul 20 2016 Dave Dykstra <dwd@fnal.gov> 1.4-1
- Use more reliable method of calculating seconds since the epoch.  It
  was off by an hour.
- Fix broken case of proxy not previously existing without --reuseonly.

* Tue Jul 19 2016 Dave Dykstra <dwd@fnal.gov> 1.3-1
- Add --reuseonly and --noreuseonly options.
- When checking for reuse, do not require the institution name to
  match the /O= in the DN.
- Allow an institution to support only kerberos authentication: don't
  prompt for password if there's no non-kerberos IdP listed.
- Remove extra newline at the end of fatal error messages.

* Fri Jul 08 2016 Dave Dykstra <dwd@fnal.gov> 1.2-1
- Try kerberos authentication first by default when the institution's
  IdP is known to support it, without a --kerberos option.
- Add --nokerberos option.
- Add support for additional default options in $CIGETCERTOPTS.
- Use getpwuid() instead of $LOGNAME for current user name.
- Avoid stack trace crash on el5 when previous outfile is empty.
- Avoid stack trace when password prompt is interrupted.
- Add wrapper script to unset PYTHONPATH and LD_LIBRARY_PATH.
- Pre-compile cigetcert python source.

* Mon Apr 04 2016 Dave Dykstra <dwd@fnal.gov> 1.1-1
- Create the output file with O_EXCL.

* Tue Mar 01 2016 Dave Dykstra <dwd@fnal.gov> 1.0-1
- Remove a pylint error and a few pylint warnings

* Fri Feb 19 2016 Dave Dykstra <dwd@fnal.gov> 0.9-1
- Add missing '/' to the beginning of the DN used as the username for
    myproxy and printed out the -v option
- Add --listinstitutions option

* Thu Feb 11 2016 Dave Dykstra <dwd@fnal.gov> 0.8-1
- Initial rpm packaging
