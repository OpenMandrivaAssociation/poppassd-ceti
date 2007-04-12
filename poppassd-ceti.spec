%define name poppassd-ceti
%define version 1.8.5
%define release 1mdk

Summary: An Eudora and NUPOP change password server
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://echelon.pl/pubs/poppassd.html
Source0: http://echelon.pl/pubs/poppassd-%{version}.tar.bz2
Source1: poppassd.pam.bz2
Source2: poppassd.xinetd.bz2
Patch2: poppassd-buildroot.patch
Patch3: poppassd-ceti-1.8-uid500.patch
License: Distributable
Provides: poppassd
Requires: pam net-tools setup tcp_wrappers sysklogd
BuildRequires: pam-devel
Group: Networking/Remote access
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
Poppassd is a daemon allowing users to change their password via Eudora 
or NUPOP using a network protocol on port 106. This package uses PAM.

Original version based on John Norstad's poppassd code. John
Norstad's program ran the regular unix "passwd" command. This version
calls PAM to change the password.

Examine the (un)install scripts with "rpm --scripts <package>" before
(de)installation. They modify some system configuration files.

(See also ftp://ftp.nwu.edu/pub/poppassd for Norstad's original code).

[Note, to log poppassd password changes, add the following line:

	local4.err 	-/var/log/poppassd.log

to your /etc/syslog.conf file.]

%prep
%setup -n poppassd-%{version}
%patch2 -p1
%patch3 -p1

%build
%serverbuild
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_sysconfdir}/pam.d \
	$RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d
make BINDIR=$RPM_BUILD_ROOT%{_sbindir} install
bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/poppassd
bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/poppassd
chmod 644 README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
%attr(0700,root,root) %{_prefix}/sbin/poppassd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/poppassd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/xinetd.d/poppassd

