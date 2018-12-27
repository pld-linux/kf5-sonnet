# TODO:
# - fix build with aspell
%define		kdeframever	5.53
%define		qtver		5.9.0
%define		kfname		sonnet

Summary:	Multi-language spell checker
Name:		kf5-%{kfname}
Version:	5.53.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	fd28bda2bd2c1c0d40e477930394ed14
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	aspell
BuildRequires:	aspell-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	hspell-devel
BuildRequires:	hunspell-devel
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	libvoikko-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	kf5-dirs
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
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/gentrigrams
%attr(755,root,root) %{_bindir}/parsetrigrams
%attr(755,root,root) %ghost %{_libdir}/libKF5SonnetCore.so.5
%attr(755,root,root) %{_libdir}/libKF5SonnetCore.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5SonnetUi.so.5
%attr(755,root,root) %{_libdir}/libKF5SonnetUi.so.*.*
%dir %{qt5dir}/plugins/kf5/sonnet
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/sonnet_aspell.so
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/sonnet_hspell.so
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/sonnet_hunspell.so
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/sonnet_voikko.so
%dir %{_datadir}/kf5/sonnet
%{_datadir}/kf5/sonnet/trigrams.map
/etc/xdg/sonnet.categories

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
