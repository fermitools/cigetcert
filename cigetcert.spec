Summary: Get an X.509 certificate with SAML ECP and store proxies
Name: cigetcert
Version: 0.8
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

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/man/man1
cp %{name} $RPM_BUILD_ROOT/%{_bindir}
gzip -c %{name}.1 >$RPM_BUILD_ROOT/%{_datadir}/man/man1/%{name}.1.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{_datadir}/man/man1/%{name}*


%changelog
* Thu Feb 11 2016 Dave Dykstra <dwd@fnal.gov> 0.8-1
- Initial rpm packaging
