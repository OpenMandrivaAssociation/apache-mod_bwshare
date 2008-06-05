#Module-Specific definitions
%define mod_name mod_bwshare
%define mod_conf 77_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Bandwidth throttling and balancing by client IP address
Name:		apache-%{mod_name}
Version:	0.2.1
Release:	%mkrel 2
Group:		System/Servers
License:	Artistic
URL:		http://www.topology.org/src/bwshare/README.html
Source0:	http://www.topology.org/src/bwshare/%{mod_name}-%{version}.zip
Source1:	http://www.topology.org/src/bwshare/%{mod_name}-%{version}.zip.asc
Source2:	%{mod_conf}
BuildRequires:	unzip
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Apache shaping module "bwshare" uses a form of "statistical shaping". This
means that the software measures the statistical behaviour of the subscriber in
the past, and uses this as a basis for controlling the current access to
resources by the user. 

The purpose of this module is to give the web site operator some control over
bandwidth utilization by individual client hosts. The "bwshare" module
temporarily blocks access by excessive users. This is aimed especially at users
who download whole websites at great speed. Excessive speed is considered bad
etiquette for search engine robots.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE2} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENCE README.html changes.html doc.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*




