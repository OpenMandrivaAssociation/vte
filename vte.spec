%define lib_major 9
%define lib_name %mklibname %{name} %{lib_major}
%define develname %mklibname -d %name

%define api 0.0
Name: vte
Version: 0.26.2
Release: %mkrel 2
Summary: A terminal emulator widget
License: LGPLv2+
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0:	vte-0.25.90-alt_meta.patch
BuildRequires: gtk+2-devel
BuildRequires: libxft-devel
BuildRequires: libmesaglu-devel
BuildRequires: ncurses-devel
BuildRequires: automake
BuildRequires: gtk-doc
BuildRequires: python-devel
BuildRequires: pygtk2.0-devel
BuildRequires: gobject-introspection-devel
BuildRequires: intltool
URL: http://www.gnome.org/

%description
VTE is a terminal emulator widget for use with GTK+ 2.0.


%package -n python-%{name}
Summary: Python binding for VTE
Group: Development/Python
Requires: %{name} >= %{version}

%description -n  python-%{name}
Python binding for VTE, a terminal emulator widget for use 
with GTK+ 2.0.


%package -n %{lib_name}
Summary: A terminal emulator widget
Group: System/Libraries
Requires: %{name} >= %{version}
Conflicts: gir-repository < 0.6.6

%description -n %{lib_name}
VTE is a terminal emulator widget for use with GTK+ 2.0. 

%package -n %develname
Summary: Files needed for developing applications which use VTE
Group: Development/C
Provides:  lib%{name}-devel = %{version}-%{release}
Provides:  %{name}-devel = %{version}-%{release}
Requires:  %{lib_name} = %{version}-%release
Requires: gtk+2-devel
Requires: ncurses-devel
Obsoletes: %mklibname -d %name 9

%description -n %develname
VTE is a terminal emulator widget for use with GTK+ 2.0.  This
package contains the files needed for building applications using VTE.

%prep
%setup -q
%apply_patches

%build

%configure2_5x --enable-shared --enable-static --libexecdir=%{_libdir}/%{name} --enable-python --enable-gtk-doc --enable-introspection

%make 

%install
rm -fr $RPM_BUILD_ROOT

%makeinstall_std

find $RPM_BUILD_ROOT/%py_platsitedir -name '*.a' | xargs rm -f
find $RPM_BUILD_ROOT/%py_platsitedir -name '*.la' | xargs rm -f
%find_lang %{name}-%api

%clean
rm -fr $RPM_BUILD_ROOT

%files -f %{name}-%api.lang
%defattr(-,root,root)
%doc COPYING HACKING NEWS README
%{_bindir}/*
%{_libdir}/%{name}
%{_libdir}/%{name}-%api
%attr(2711,root,utmp) %{_libdir}/%{name}/gnome-pty-helper
%{_datadir}/%{name}

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.%{lib_major}*
%_libdir/girepository-1.0/Vte-0.0.typelib

%files -n %develname
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/*.a
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%_datadir/pygtk/2.0/defs/vte.defs
%_datadir/gir-1.0/Vte-0.0.gir

%files -n python-%{name}
%defattr(-,root,root)
%py_platsitedir/gtk-2.0/vtemodule.so
