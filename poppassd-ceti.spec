Summary:	An Eudora and NUPOP change password server
Name:		poppassd-ceti
Version:	1.8.5
Release:	%mkrel 3
Group:		Networking/Remote access
License:	Distributable
URL:		http://echelon.pl/pubs/poppassd.html
Source0:	http://echelon.pl/pubs/poppassd-%{version}.tar.bz2
Source1:	poppassd.pam.bz2
Source2:	poppassd.xinetd.bz2
Patch2:		poppassd-buildroot.patch
Patch3:		poppassd-ceti-1.8-uid500.patch
Provides:	poppassd
Requires:	net-tools
Requires:	pam
Requires:	tcp_wrappers
BuildRequires:	pam-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_sysconfdir}/xinetd.d

make BINDIR=%{buildroot}%{_sbindir} install

bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/pam.d/poppassd
bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/xinetd.d/poppassd
chmod 644 README

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/poppassd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/xinetd.d/poppassd
%attr(0700,root,root) %{_sbindir}/poppassd
