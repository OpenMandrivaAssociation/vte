%define url_ver %(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1
%define _disable_lto 1
%define debug_package %{nil}

%define api	0.0
%define major	9
%define libname %mklibname %{name} %{api} %{major}
%define girname %mklibname %{name}-gir %{api}
%define devname %mklibname -d %{name}

Summary:	A terminal emulator widget
Name:		vte
Version:	0.28.2
Release:	18
License:	LGPLv2+
Group:		System/Libraries
URL:		https://www.gnome.org/
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Patch1:		honey-I-shrank-the-terminal.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=663779
Patch2:		vte-alt-meta-confusion.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=688456
Patch3:		0001-widget-Only-show-the-cursor-on-motion-if-moved.patch
Patch4:		vte-aarch64.patch
Patch5:		vte-python-bugfixes.patch
Patch6:		vte-0.28.0-link.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.20.0
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(x11)

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

%description -n %{libname}
VTE is a terminal emulator widget for use with GTK+ 2.0.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}vte9 < 0.28.2-2

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Summary:	Files needed for developing applications which use VTE
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Obsoletes:	%{_lib}vte9-devel

%description -n %{devname}
VTE is a terminal emulator widget for use with GTK+ 2.0.  This
package contains the files needed for building applications using VTE.

%prep
%setup -q
%autopatch -p1

%build
export CFLAGS=-fno-lto
export PYTHON=%__python2

%configure2_5x \
	--enable-shared \
	--disable-static \
	--libexecdir=%{_libdir}/%{name} \
	--enable-python \
	--enable-gtk-doc \
	--enable-introspection \
	--with-gtk=2.0

%make

%install
%makeinstall_std

find %{buildroot}/%{py_platsitedir} -name '*.a' | xargs rm -f
find %{buildroot}/ -name '*.la' | xargs rm -f

%find_lang %{name}-%{api}

%files -f %{name}-%{api}.lang
%doc COPYING HACKING NEWS README
%{_bindir}/*
%{_datadir}/vte/termcap-0.0/xterm
%dir %{_libdir}/%{name}
%attr(2711,root,utmp) %{_libdir}/%{name}/gnome-pty-helper

%files -n python-%{name}
# % {py_platsitedir}/gtk-2.0/vtemodule.so

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Vte-%{api}.typelib

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/Vte-%{api}.gir
