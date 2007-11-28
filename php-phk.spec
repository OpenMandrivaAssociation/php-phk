%define modname phk
%define dirname %{modname}
%define soname %{modname}.so
%define inifile Z99_%{modname}.ini

Summary:	PHK Accelerator extension
Name:		php-%{modname}
Version:	1.1.0
Release:	%mkrel 1
Group:		Development/PHP
License:	PHP License
URL:		http://phk.tekwire.net/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:		phk-buildfix.diff
BuildRequires:  php-devel >= 3:5.2.0
Suggests:	php-apc
Suggests:	php-eaccelerator
Suggests:	php-memcache
Suggests:	php-xcache
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Transparently makes PHK runtime code faster.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 .libs/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc tests CREDITS LICENSE package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

