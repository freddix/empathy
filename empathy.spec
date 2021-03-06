Summary:	Telepathy client for GNOME
Name:		empathy
Version:	3.12.7
Release:	1
License:	GPL
Group:		X11/Applications/Communications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/empathy/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	b86c915c2465203e0ff1443c5987560a
Patch0:		%{name}-configure.patch
URL:		http://live.gnome.org/Empathy
BuildRequires:	cheese-devel >= 3.12.0
BuildRequires:	clutter-gst-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	enchant-devel
BuildRequires:	evolution-data-server-devel >= 3.12.0
BuildRequires:	farstream-devel
BuildRequires:	folks-devel
BuildRequires:	gcr-devel
BuildRequires:	gnome-online-accounts-devel >= 3.12.0
BuildRequires:	gsettings-desktop-schemas-devel >= 3.12.0
BuildRequires:	gtk+3-webkit-devel >= 2.4.0
BuildRequires:	intltool
BuildRequires:	iso-codes
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libchamplain-gtk-devel
BuildRequires:	libgnome-keyring-devel >= 3.12.0
BuildRequires:	libnotify-devel
BuildRequires:	libsoup-devel >= 2.46.0
BuildRequires:	libxml2-devel
BuildRequires:	telepathy-farstream-devel
BuildRequires:	telepathy-logger-devel
BuildRequires:	telepathy-mission-control-devel
BuildRequires:	yelp-tools
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	gtk+-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	folks
Requires:	gnome-online-accounts
Requires:	gsettings-desktop-schemas
Requires:	telepathy-logger
Requires:	telepathy-mission-control
Requires:	telepathy-service
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
Empathy consists of a rich set of reusable instant messaging widgets
and a GNOME client using those widgets. It uses Telepathy and Nokia's
Mission Control, and reuses Gossip's UI. The main goal is to permit
desktop integration by providing libempathy and libempathy-gtk
libraries.

%package -n nautilus-sendto-empathy
Summary:	nautilus-sendto Empathy plugin
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus-sendto

%description -n nautilus-sendto-empathy
A nautilus-sendto plugin for sending files via Empathy.

%prep
%setup -q
%patch0 -p1

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-static		\
	--enable-gudev			\
	--with-cheese
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/GConf
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/empathy
%attr(755,root,root) %{_bindir}/empathy-accounts
%attr(755,root,root) %{_bindir}/empathy-debugger
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/empathy-auth-client
%attr(755,root,root) %{_libexecdir}/empathy-call
%attr(755,root,root) %{_libexecdir}/empathy-chat
%attr(755,root,root) %{_libdir}/mission-control-plugins.0/mcp-account-manager-goa.so

%attr(755,root,root) %{_libdir}/empathy/libempathy-%{version}.so
%attr(755,root,root) %{_libdir}/empathy/libempathy-gtk-%{version}.so

%{_datadir}/adium
%{_datadir}/%{name}
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.Auth.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.Call.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.Chat.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Empathy.FileTransfer.service
%{_datadir}/glib-2.0/schemas/org.gnome.Empathy.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.telepathy-account-widgets.gschema.xml

%{_datadir}/telepathy/clients/Empathy.Auth.client
%{_datadir}/telepathy/clients/Empathy.Call.client
%{_datadir}/telepathy/clients/Empathy.Chat.client
%{_datadir}/telepathy/clients/Empathy.FileTransfer.client

%{_iconsdir}/hicolor/*/apps/*
%{_desktopdir}/*.desktop

%{_mandir}/man1/empathy*.1*

