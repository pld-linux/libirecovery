#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	Library and utility to talk to iBoot/iBSS via USB
Name:		libirecovery
Version:	0.1.1
Release:	0.1
License:	LGPL v2.1
Group:		Libraries
Source0:	https://github.com/libirecovery/libirecovery/archive/master.tar.gz?/%{name}.tgz
# Source0-md5:	c285877601bd5496c194a34959f29754
URL:		http://www.libirecovery.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libirecovery is a cross-platform library which implements
communication to iBoot/iBSS found on Apple's iOS devices via USB. A
command-line utility is also provided.

%package devel
Summary:	Header files for libirecovery library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libirecovery
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libirecovery library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libirecovery.

%package static
Summary:	Static libirecovery library
Summary(pl.UTF-8):	Statyczna biblioteka libirecovery
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libirecovery library.

%description static -l pl.UTF-8
Statyczna biblioteka libirecovery.

%prep
%setup -qc
mv libirecovery-*/* .

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	%{!?with_openssl:--disable-openssl} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/irecovery
%attr(755,root,root) %{_libdir}/libirecovery.so.*.*.*
%ghost %{_libdir}/libirecovery.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/libirecovery.h
%{_libdir}/libirecovery.so
%{_pkgconfigdir}/libirecovery.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libirecovery.a
%endif
