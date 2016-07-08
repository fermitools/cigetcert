Summary: Get an X.509 certificate with SAML ECP and store proxies
Name: cigetcert
Version: 1.2
Release: 1%{?dist}
License: BSD
Group: Applications/System
URL: http://redmine.fnal.gov/projects/fermitools/wiki/cigetcert
# download with:
# $ curl -o cigetcert-%{version}.tar.gz \
#    https://codeload.github.com/fermitools/cigetcert/tar.gz/%{version}
Source0: %{name}-%{version}.tar.gz
Requires: python
Requires: m2crypto
Requires: pyOpenSSL
Requires: python-lxml
Requires: python-kerberos
BuildRequires: python

BuildArch: noarch
%if %{?rhel}%{!?rhel:6} <= 5
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%endif

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
cp %{name}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}
cp %{name} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/%{name}.py
python -Em compileall -d %{_libexecdir}/%{name} $RPM_BUILD_ROOT%{_libexecdir}/%{name}
gzip -c %{name}.1 >$RPM_BUILD_ROOT%{_datadir}/man/man1/%{name}.1.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/man/man1/%{name}*


%changelog
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

%changelog
* Tue Mar 01 2016 Dave Dykstra <dwd@fnal.gov> 1.0-1
- Remove a pylint error and a few pylint warnings

* Fri Feb 19 2016 Dave Dykstra <dwd@fnal.gov> 0.9-1
- Add missing '/' to the beginning of the DN used as the username for
    myproxy and printed out the -v option
- Add --listinstitutions option

* Thu Feb 11 2016 Dave Dykstra <dwd@fnal.gov> 0.8-1
- Initial rpm packaging
