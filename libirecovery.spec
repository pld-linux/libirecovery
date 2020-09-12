#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	Library and utility to talk to iBoot/iBSS via USB
Summary(pl.UTF-8):	Biblioteka i narzędzie do komunikacji z iBoot/iBSS po USB
Name:		libirecovery
Version:	1.0.0
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://libimobiledevice.org/
Source0:	https://github.com/libimobiledevice/libirecovery/releases/download/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	ff4aff474e8d58f70b55091519c4015b
Patch0:		%{name}-sh.patch
URL:		https://github.com/libimobiledevice/libirecovery
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libusb-devel >= 1.0.3
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
Requires:	libusb >= 1.0.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libirecovery is a cross-platform library which implements
communication to iBoot/iBSS found on Apple's iOS devices via USB. A
command-line utility is also provided.

%description -l pl.UTF-8
libirecovery to wieloplatformowa biblioteka implementująca komunikację
po USB z iBoot/iBSS, które można spotkać w urządzeniach z systemem iOS
Apple'a. Dołączone jest także narzędzie działające z linii poleceń.

%package devel
Summary:	Header files for libirecovery library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libirecovery
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libusb-devel >= 1.0.3

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
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_openssl:--disable-openssl} \
	%{!?with_static_libs:--disable-static} \
	--disable-silent-rules \
	--with-udev \
	--with-udevrule='OWNER="root", GROUP="usb", MODE="0660"' \
	--with-udevrulesdir=/lib/udev/rules.d

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libirecovery-1.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/irecovery
%attr(755,root,root) %{_libdir}/libirecovery-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libirecovery-1.0.so.3
/lib/udev/rules.d/39-libirecovery.rules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libirecovery-1.0.so
%{_includedir}/libirecovery.h
%{_pkgconfigdir}/libirecovery-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libirecovery-1.0.a
%endif
