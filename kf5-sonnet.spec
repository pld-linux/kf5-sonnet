# TODO:
# - dir /usr/include/KF5 not packaged
# /usr/lib/qt5/qml/org/kde not packaged
# /usr/lib/qt5/plugins/kf5
# /usr/share/kf5

%define         _state          stable
%define		orgname		sonnet

Summary:	Multi-language spell checker
Name:		kf5-%{orgname}
Version:	5.0.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/frameworks/%{version}/%{orgname}-%{version}.tar.xz
# Source0-md5:	b5608009ca1d34e6fdfd4f89c9752eef
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel >= 5.3.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	aspell-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	hspell-devel
BuildRequires:	hunspell-devel
BuildRequires:	kf5-extra-cmake-modules >= 1.0.0
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
Sonnet is a plugin-based spell checking library for Qt-based
applications. It supports several different plugins, including HSpell,
Enchant, ASpell and HUNSPELL.

It also supports automated language detection, based on a combination
of different algorithms.

The simplest way to use Sonnet in your application is to use the
SpellCheckDecorator class on your QTextEdit.

%package devel
Summary:	Header files for %{orgname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{orgname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{orgname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{orgname}.

%prep
%setup -q -n %{orgname}-%{version}

%build
install -d build
cd build
%cmake \
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DKCFG_INSTALL_DIR=%{_datadir}/config.kcfg \
	-DPLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQT_PLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQML_INSTALL_DIR=%{qt5dir}/qml \
	-DIMPORTS_INSTALL_DIR=%{qt5dirs}/imports \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_LIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_INCLUDE_INSTALL_DIR=%{_includedir} \
	-DECM_MKSPECS_INSTALL_DIR=%{qt5dir}/mkspecs/modules \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{orgname}5_qt --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{orgname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %ghost %{_libdir}/libKF5SonnetCore.so.5
%attr(755,root,root) %{_libdir}/libKF5SonnetCore.so.5.0.0
%attr(755,root,root) %ghost %{_libdir}/libKF5SonnetUi.so.5
%attr(755,root,root) %{_libdir}/libKF5SonnetUi.so.5.0.0
%dir %{qt5dir}/plugins/kf5/sonnet
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/aspell.so
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/hspell.so
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/hunspell.so
%dir %{_datadir}/kf5/sonnet
%{_datadir}/kf5/sonnet/trigrams.map

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/SonnetCore
%{_includedir}/KF5/SonnetUi
%{_includedir}/KF5/sonnet_version.h
%{_libdir}/cmake/KF5Sonnet
%attr(755,root,root) %{_libdir}/libKF5SonnetCore.so
%attr(755,root,root) %{_libdir}/libKF5SonnetUi.so
%{qt5dir}/mkspecs/modules/qt_SonnetCore.pri
%{qt5dir}/mkspecs/modules/qt_SonnetUi.pri
