%define api 0.0
%define major 9
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name:		vte
Version:	0.28.2
Release:	1
Summary:	A terminal emulator widget
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz
Patch0:		vte-0.25.90-alt_meta.patch
Patch1:		vte-0.28.0-link.patch
Patch2:		vte-0.28.2-scale.patch
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.20.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	automake
BuildRequires:	gtk-doc
BuildRequires:	python-devel
BuildRequires:	pygtk2.0-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	intltool

%description
VTE is a terminal emulator widget for use with GTK+ 2.0.

%package -n python-%{name}
Summary:	Python binding for VTE
Group:		Development/Python
Requires:	%{name} >= %{version}-%{release}

%description -n python-%{name}
Python binding for VTE, a terminal emulator widget for use 
with GTK+ 2.0.

%package -n %{libname}
Summary:	A terminal emulator widget
Group:		System/Libraries
Requires:	%{name} >= %{version}-%{release}
Conflicts:	gir-repository < 0.6.6

%description -n %{libname}
VTE is a terminal emulator widget for use with GTK+ 2.0. 

%package -n %{develname}
Summary:	Files needed for developing applications which use VTE
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname -d %name 9

%description -n %{develname}
VTE is a terminal emulator widget for use with GTK+ 2.0.  This
package contains the files needed for building applications using VTE.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--enable-shared \
	--disable-static \
	--libexecdir=%{_libdir}/%{name} \
	--enable-python \
	--enable-gtk-doc \
	--enable-introspection \
	--with-gtk=2.0

%make LIBS='-lm -lncurses -lutil -lgmodule-2.0'

%install
%makeinstall_std

find %{buildroot}/%{py_platsitedir} -name '*.a' | xargs rm -f
find %{buildroot}/ -name '*.la' | xargs rm -f

%find_lang %{name}-%{api}

%files -f %{name}-%{api}.lang
%doc COPYING HACKING NEWS README
%{_bindir}/*
%dir %{_libdir}/%{name}
%attr(2711,root,utmp) %{_libdir}/%{name}/gnome-pty-helper
%{_datadir}/%{name}

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/girepository-1.0/Vte-%{api}.typelib

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/pygtk/2.0/defs/vte.defs
%{_datadir}/gir-1.0/Vte-0.0.gir

%files -n python-%{name}
%{py_platsitedir}/gtk-2.0/vtemodule.so
