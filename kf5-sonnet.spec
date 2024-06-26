#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# - fix build with aspell
%define		kdeframever	5.116
%define		qtver		5.15.2
%define		kfname		sonnet

Summary:	Multi-language spell checker
Summary(pl.UTF-8):	Wielojęzyczne narzędzie do sprawdzania pisowni
Name:		kf5-%{kfname}
Version:	5.116.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	baeb09e7fad7bdd101e662ca17dae770
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	aspell
BuildRequires:	aspell-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	hspell-devel
BuildRequires:	hunspell-devel
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	libvoikko-devel
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
Sonnet is a plugin-based spell checking library for Qt-based
applications. It supports several different plugins, including HSpell,
ASpell and HUNSPELL.

It also supports automated language detection, based on a combination
of different algorithms.

The simplest way to use Sonnet in your application is to use the
SpellCheckDecorator class on your QTextEdit.

%description -l pl.UTF-8
Sonnet to oparta na wtyczkach biblioteka do sprawdzania pisowni dla
aplikacji opartych na Qt. Obsługuje kilka różnych wtyzek, w tym
HSpell, ASpell i HUNSPELL.

Pozwala automatycznie wykrywać język w oparciu o połączenie różnych
algorytmów.

Najprostszy sposób użycia Sonneta w aplikacji to użycie klasy
SpellCheckDecorator w obiekcie QTextEdit.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qtver}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/gentrigrams
%attr(755,root,root) %{_bindir}/parsetrigrams
%ghost %{_libdir}/libKF5SonnetCore.so.5
%attr(755,root,root) %{_libdir}/libKF5SonnetCore.so.*.*
%ghost %{_libdir}/libKF5SonnetUi.so.5
%attr(755,root,root) %{_libdir}/libKF5SonnetUi.so.*.*
%dir %{qt5dir}/plugins/kf5/sonnet
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/sonnet_aspell.so
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/sonnet_hspell.so
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/sonnet_hunspell.so
%attr(755,root,root) %{qt5dir}/plugins/kf5/sonnet/sonnet_voikko.so
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/sonnet/libsonnetquickplugin.so
%dir %{_libdir}/qt5/qml/org/kde/sonnet
%{_libdir}/qt5/qml/org/kde/sonnet/plugins.qmltypes
%{_libdir}/qt5/qml/org/kde/sonnet/qmldir
%attr(755,root,root) %{qt5dir}/plugins/designer/sonnetui5widgets.so
%{_datadir}/qlogging-categories5/sonnet.categories
%{_datadir}/qlogging-categories5/sonnet.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/SonnetCore
%{_includedir}/KF5/SonnetUi
%{_includedir}/KF5/Sonnet
%{_libdir}/cmake/KF5Sonnet
%{_libdir}/libKF5SonnetCore.so
%{_libdir}/libKF5SonnetUi.so
%{qt5dir}/mkspecs/modules/qt_SonnetCore.pri
%{qt5dir}/mkspecs/modules/qt_SonnetUi.pri
